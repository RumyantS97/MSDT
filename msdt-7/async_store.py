import asyncio
import random
import time
import logging

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Order:
    def __init__(self, order_id: int, items: list, total_amount: float):
        self.order_id = order_id
        self.items = items
        self.total_amount = total_amount
        self.status = "created"

class OrderProcessor:
    async def verify_payment(self, order: Order):
        """Check order payment"""
        verification_time = random.uniform(0.5, 2)
        await asyncio.sleep(verification_time)
        
        if random.random() < 0.1:  # 10% refuce chance
            raise Exception(f"Order payment error {order.order_id}")
        
        logging.info(f"Order payment success {order.order_id}")
        return True

    async def check_inventory(self, order: Order):
        """Check staff availability"""
        check_time = random.uniform(0.3, 1.5)
        await asyncio.sleep(check_time)
        
        if random.random() < 0.1:  # 10% out of stock chance
            raise Exception(f"Product out of stock for order {order.order_id}")
        
        logging.info(f"Products are in stock for order {order.order_id}")
        return True

    async def process_shipping(self, order: Order):
        """Shipping processing"""
        shipping_time = random.uniform(1, 3)
        await asyncio.sleep(shipping_time)
        
        if random.random() < 0.1:  # 10% shipping problems chance
            raise Exception(f"Problems with shipping for order {order.order_id}")
        
        logging.info(f"Delivery processed for order {order.order_id}")
        return True

    async def process_order(self, order: Order):
        """Full order processing"""
        try:
            await self.verify_payment(order)
            await self.check_inventory(order)
            await self.process_shipping(order)
            
            order.status = "completed"
            logging.info(f"Order {order.order_id} successfully processed")
            return True
            
        except Exception as e:
            order.status = "failed"
            logging.error(f"Error for processing order {order.order_id}: {str(e)}")
            return False

async def process_orders(orders: list):
    """Async order processing"""
    processor = OrderProcessor()
    tasks = [processor.process_order(order) for order in orders]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def main():
    # Test order creation
    test_orders = [
        Order(1, ["Phone", "Case"], 1000),
        Order(2, ["Laptop"], 2000),
        Order(3, ["Headphones"], 300),
        Order(4, ["Tablet", "Keyboard"], 1500),
        Order(5, ["Mouse"], 50)
    ]

    logging.info("Orders process start")
    start_time = time.time()

    # Orders processing
    results = await process_orders(test_orders)

    # Analysis
    success_count = sum(1 for result in results if result is True)
    fail_count = len(results) - success_count
    total_time = time.time() - start_time

    # Statistics
    logging.info("\n=== Orders processing statistics ===")
    logging.info(f"Total orders: {len(test_orders)}")
    logging.info(f"Success orders: {success_count}")
    logging.info(f"Failed: {fail_count}")
    logging.info(f"Total processing time: {total_time:.2f} seconds")

    # Detailed order information
    logging.info("\n=== Detailed order information ===")
    for order in test_orders:
        logging.info(f"Order {order.order_id}: Status - {order.status}")

    return {
        'total_orders': len(test_orders),
        'successful': success_count,
        'failed': fail_count,
        'processing_time': total_time
    }

async def run_with_retry(coro, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return await coro
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            logging.warning(f"Attempt {attempt + 1} is not successful. Retry...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        results = asyncio.run(main())
        
        # Summary
        print("\n=== Summart ===")
        print(f"Total processed order: {results['total_orders']}")
        print(f"Successfull: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Total time: {results['processing_time']:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\nProgram stopped by user interrupt")
    except Exception as e:
        print(f"\nError: {str(e)}")