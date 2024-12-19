def find_in_2d_array(array, target):
    for row_idx, row in enumerate(array):
        for col_idx, value in enumerate(row):
            if value == target:
                return row_idx, col_idx
    return None