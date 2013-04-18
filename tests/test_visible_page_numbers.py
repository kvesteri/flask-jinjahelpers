from flask_jinjahelpers import visible_page_numbers


class TestVisiblePageNumbers(object):
    def test_should_calculate_windowed_visible_pages(self):
        visible = visible_page_numbers(page=7, pages=42)
        assert visible == [1, '...', 4, 5, 6, 7, 8, 9, 10, '...', 42]

    def test_should_eliminate_small_gaps(self):
        visible = visible_page_numbers(page=6, pages=11)
        assert visible == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def test_should_adjust_upper_limit_if_lower_is_out_of_bounds(self):
        visible = visible_page_numbers(page=1, pages=42)
        assert visible == [1, 2, 3, 4, 5, 6, 7, '...', 42]

    def test_should_adjust_lower_limit_if_upper_is_out_of_bounds(self):
        visible = visible_page_numbers(page=40, pages=42)
        assert visible == [1, '...', 36, 37, 38, 39, 40, 41, 42]
