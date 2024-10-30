import os
import sys
import torch
import shutil
from typing import List
import pandas as pd
import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(ROOT_DIR)

from LSTM_base.pipleline_LSTM_base import PipelineTrainLSTMBase


class PipelineTrainLSTMSymbolDay(PipelineTrainLSTMBase):
    def __init__(
        self,
        access_key_admin=None,
        secret_access_key_admin=None,
        endpoint_url=None,
        BACKET_S3=None,
        access_key=None,
        secret_access_key=None,
    ):
        super().__init__(
            access_key_admin=access_key_admin,
            secret_access_key_admin=secret_access_key_admin,
            endpoint_url=endpoint_url,
            BACKET_S3=BACKET_S3,
            access_key=access_key,
            secret_access_key=secret_access_key,
            epochs=1,
            lr=0.001,
            max_lr=1e-3,
        )

        self.n_features = 15
        self.batch_size = 256
        self.s3_path_main = "datalake/marketdata/train_data_new/"
        self.s3_path_model = (
            f"{self.s3_path_main}LSTM2_models/e{str(self.epochs)}_lr{str(self.lr).replace('0.', '')}_mlr{str(self.max_lr).replace('0.', '')}/"
        )
        self.s3_dataset_path = f"{self.s3_path_main}LSTM2/"
        self.local_path = "train_data_LSTM2"

        logging.basicConfig(level="INFO", format="%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.logger = logging.getLogger(os.path.basename(__file__))

    def testFileLoader(self, files: List[str]):
        len_file = len(files)
        count_files = 0

        while count_files < len_file:
            file = files[count_files]
            symbol_candles_arr = self.get_dataset(f"{file}_candles.pt", f"{self.s3_dataset_path}test_data")
            symbol_tone_arr = self.get_dataset(f"{file}_tone.pt", f"{self.s3_dataset_path}test_data")
            count_files += 1
            yield (symbol_candles_arr.float(), symbol_tone_arr.float(), file)

    def fileLoader(self, files: List[str], file_type="train_data"):
        len_file = len(files)
        count_files = 0

        while count_files < len_file:
            file = files[count_files]
            symbol_candles_arr = self.get_dataset(f"{file}_candles.pt", f"{self.s3_dataset_path}{file_type}")
            symbol_tone_arr = self.get_dataset(f"{file}_tone.pt", f"{self.s3_dataset_path}{file_type}")
            count_files += 1

            while symbol_candles_arr.shape[0] >= self.batch_size:
                symbol_candles_arr_i = symbol_candles_arr[:self.batch_size]
                symbol_candles_arr = symbol_candles_arr[self.batch_size:]
                symbol_tone_arr_i = symbol_tone_arr[:self.batch_size]
                symbol_tone_arr = symbol_tone_arr[self.batch_size:]
                yield (symbol_candles_arr_i.float(), symbol_tone_arr_i.float())

    def start(self):
        self.logger.info(f"GPU: {torch.cuda.is_available()}")
        self.logger.info(f"Counts epochs: {self.epochs}, lr: {self.lr}, max lr: {self.max_lr}")

        s3_files_train = self.s3_service.get_files_by_type(f"{self.s3_dataset_path}train_data", ".pt")
        s3_files_train = list(set([i.replace("_tone.pt", "").replace("_candles.pt", "") for i in s3_files_train]))
        s3_files_val = self.s3_service.get_files_by_type(f"{self.s3_dataset_path}val_data", ".pt")
        s3_files_val = list(set([i.replace("_tone.pt", "").replace("_candles.pt", "") for i in s3_files_val]))
        s3_files_test = self.s3_service.get_files_by_type(f"{self.s3_dataset_path}test_data", ".pt")
        s3_files_test = list(set([i.replace("_tone.pt", "").replace("_candles.pt", "") for i in s3_files_test]))

        model = self.model_service_base.create_model(input_size=self.n_features, hidden_size=30, num_layers=5, output_size=2)
        pytorch_total_params = sum(p.numel() for p in model.parameters())

        if torch.cuda.is_available():
            model = model.to("cuda")

        criterion, optimizer, scheduler = self.model_service_base.get_params(
            model_params=model.parameters(), lr=self.lr, max_lr=self.max_lr, steps_per_epoch=1_000_000, epochs=self.epochs, anneal_strategy="linear"
        )

        df_test = pd.DataFrame(columns=["symbol", "acc", "mse"])

        for epoch in range(self.epochs):
            model = self.train(criterion, optimizer, scheduler, model, s3_files_train, epoch)
            model = self.validation(model, s3_files_val)
        model, df_test = self.test(model, s3_files_test, df_test)

        if not os.path.exists(self.local_path):
            os.mkdir(self.local_path)

        self.s3_service.load_df_csv_to_s3(df_test, self.local_path, "symbol_test.csv", f"{self.s3_path_model}plt/")
        self.model_service_base.save_model(model, "ready_model.pt", self.local_path, f"{self.s3_path_model}models/")
        self.save_single_plot(f"{self.local_path}/sheduler_OneCycleLR_c.jpg", self.shed_list, "sheduler_OneCycleLR_c.jpg", f"{self.s3_path_model}plt/")
        self.save_single_plot(f"{self.local_path}/pair_loss.jpg", self.loss_list, "pair_loss.jpg", f"{self.s3_path_model}plt/")
        self.save_multi_plot(f"{self.local_path}/symbol_acc.jpg", [self.acc_list_train, self.acc_list_val], "symbol_acc.jpg", f"{self.s3_path_model}plt/")

        shutil.rmtree(self.local_path, ignore_errors=True)


if __name__ == "__main__":
    pipeline_train_lstm_symbol_day = PipelineTrainLSTMSymbolDay(
        access_key_admin=os.environ["ACCESS_KEY_READER_ADMIN"],
        secret_access_key_admin=os.environ["SECRET_ACCESS_KEY_READER_ADMIN"],
        endpoint_url=os.environ["ENDPOINT_URL"],
        BACKET_S3=os.environ["BACKET_S3"],
        access_key=os.environ["ACCESS_KEY_READER"],
        secret_access_key=os.environ["SECRET_ACCESS_KEY_READER"],
    )
    pipeline_train_lstm_symbol_day.start()
