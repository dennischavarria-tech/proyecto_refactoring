import pytest

from exceptions import InvalidInputError
from validators import (
    validate_menu_option,
    validate_search_query,
    validate_movie_title,
    validate_actor_name,
    validate_series_name,
    validate_year,
    validate_timeout,
    validate_api_url,
    validate_filename,
    validate_positive_integer,
    validate_non_empty_string,
    sanitize_input,
)


class TestValidateSearchQuery:
    def test_valid_search_query(self):
        result = validate_search_query("The Matrix")
        assert result == "The Matrix"

    def test_empty_query_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_search_query("")
        assert "no puede estar vacio" in str(exc_info.value)

    def test_whitespace_only_query_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_search_query("   ")

    def test_query_too_short_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_search_query("")

    def test_query_too_long_raises_error(self):
        long_query = "a" * 201
        with pytest.raises(InvalidInputError) as exc_info:
            validate_search_query(long_query)
        assert "200 caracteres" in str(exc_info.value)

    def test_query_with_invalid_chars_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_search_query("Test<script>")
        assert "caracteres no permitidos" in str(exc_info.value)

    def test_query_with_valid_special_chars(self):
        result = validate_search_query("The Matrix - Reloaded")
        assert result == "The Matrix - Reloaded"

    def test_query_strips_whitespace(self):
        result = validate_search_query("  The Matrix  ")
        assert result == "The Matrix"

    @pytest.mark.parametrize(
        "valid_query",
        [
            "The Matrix",
            "Inception",
            "Pulp Fiction",
            "The Godfather Part II",
            "12 Angry Men",
            "Schindler's List",
        ],
    )
    def test_valid_queries_parametrized(self, valid_query):
        result = validate_search_query(valid_query)
        assert result == valid_query


class TestValidateMovieTitle:
    def test_valid_movie_title(self):
        result = validate_movie_title("Inception")
        assert result == "Inception"

    def test_empty_movie_title_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_movie_title("")


class TestValidateActorName:
    def test_valid_actor_name(self):
        result = validate_actor_name("Leonardo DiCaprio")
        assert result == "Leonardo DiCaprio"

    def test_empty_actor_name_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_actor_name("")


class TestValidateSeriesName:
    def test_valid_series_name(self):
        result = validate_series_name("Breaking Bad")
        assert result == "Breaking Bad"

    def test_empty_series_name_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_series_name("")


class TestValidateYear:
    def test_valid_year(self):
        result = validate_year("2000")
        assert result == 2000

    def test_year_too_old_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_year("1887")
        assert "1888" in str(exc_info.value)

    def test_year_too_new_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_year("2101")
        assert "2100" in str(exc_info.value)

    def test_non_numeric_year_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_year("abc")
        assert "numero" in str(exc_info.value)

    def test_empty_year_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_year("")

    def test_year_boundary_low(self):
        result = validate_year("1888")
        assert result == 1888

    def test_year_boundary_high(self):
        result = validate_year("2100")
        assert result == 2100


class TestValidateTimeout:
    def test_valid_timeout(self):
        result = validate_timeout("30")
        assert result == 30

    def test_timeout_too_low_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_timeout("0")
        assert "1 y 300" in str(exc_info.value)

    def test_timeout_too_high_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_timeout("301")
        assert "1 y 300" in str(exc_info.value)

    def test_non_numeric_timeout_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_timeout("abc")
        assert "numero" in str(exc_info.value)

    def test_empty_timeout_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_timeout("")

    def test_timeout_boundary_low(self):
        result = validate_timeout("1")
        assert result == 1

    def test_timeout_boundary_high(self):
        result = validate_timeout("300")
        assert result == 300


class TestValidateFilename:
    def test_valid_filename(self):
        result = validate_filename("test_file.json")
        assert result == "test_file.json"

    def test_filename_with_dangerous_chars_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_filename("test<file>.json")
        assert "caracteres no permitidos" in str(exc_info.value)

    def test_filename_too_long_raises_error(self):
        long_name = "a" * 256
        with pytest.raises(InvalidInputError) as exc_info:
            validate_filename(long_name)
        assert "255 caracteres" in str(exc_info.value)

    def test_filename_with_path_traversal_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_filename("../etc/passwd")
        assert "no permitidos" in str(exc_info.value) or "no puede contener" in str(exc_info.value)

    def test_empty_filename_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_filename("")

    def test_filename_with_slash_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_filename("path/to/file")

    def test_filename_with_backslash_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_filename("path\\to\\file")


class TestValidateApiUrl:
    def test_valid_http_url(self):
        result = validate_api_url("http://api.example.com")
        assert result == "http://api.example.com"

    def test_valid_https_url(self):
        result = validate_api_url("https://api.example.com")
        assert result == "https://api.example.com"

    def test_invalid_url_scheme_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_api_url("ftp://api.example.com")
        assert "http:// o https://" in str(exc_info.value)

    def test_url_too_long_raises_error(self):
        long_url = "http://" + "a" * 500
        with pytest.raises(InvalidInputError) as exc_info:
            validate_api_url(long_url)
        assert "500 caracteres" in str(exc_info.value)

    def test_empty_url_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_api_url("")


class TestValidatePositiveInteger:
    def test_valid_positive_integer(self):
        result = validate_positive_integer("42")
        assert result == 42

    def test_zero_is_valid(self):
        result = validate_positive_integer("0")
        assert result == 0

    def test_negative_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_positive_integer("-5")

    def test_non_numeric_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_positive_integer("abc")

    def test_empty_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_positive_integer("")


class TestValidateNonEmptyString:
    def test_valid_string(self):
        result = validate_non_empty_string("test")
        assert result == "test"

    def test_empty_string_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_non_empty_string("")

    def test_whitespace_only_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_non_empty_string("   ")

    def test_strips_whitespace(self):
        result = validate_non_empty_string("  test  ")
        assert result == "test"


class TestSanitizeInput:
    def test_sanitize_removes_dangerous_chars(self):
        result = sanitize_input('<script>alert("xss")</script>')
        assert "<" not in result
        assert ">" not in result
        assert '"' not in result

    def test_sanitize_strips_whitespace(self):
        result = sanitize_input("  test  ")
        assert result == "test"

    def test_sanitize_empty_string(self):
        result = sanitize_input("")
        assert result == ""

    def test_sanitize_preserves_valid_chars(self):
        result = sanitize_input("The Matrix: Reloaded")
        assert result == "The Matrix: Reloaded"


class TestValidateMenuOption:
    def test_valid_menu_option(self):
        result = validate_menu_option("1", ["1", "2", "3"])
        assert result == "1"

    def test_invalid_menu_option_raises_error(self):
        with pytest.raises(InvalidInputError) as exc_info:
            validate_menu_option("5", ["1", "2", "3"])
        assert "no valida" in str(exc_info.value)

    def test_empty_menu_option_raises_error(self):
        with pytest.raises(InvalidInputError):
            validate_menu_option("", ["1", "2", "3"])
