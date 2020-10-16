# Text-searcher

![logo](resources/images/logo.png)

Text-searcher is a small Python console program and module for text searching.  
It searches text in given directory in files with given extensions (all text-files type supported  
like txt, csv, log).

## Installation

1. Clone the repo

    ```bash
    git clone https://github.com/tomaszkyc/text-searcher.git
    ```

2. Check if you have installed Python 3.8 or later release.

## Usage

To find test "Lorem Ipsum" in folder with path "test_dir" and extensions txt and csv:
```bash
python text_searcher.py -d "test_dir" -t "Lorem Ipsum" -e txt csv
```
As a result of command you can check in the output filepath and number of text occurences.  
Number of occurences are sorted descending.
```bash
Inside file test_dir\another_dir\another_test_file.csv text occured 19 times
Inside file test_dir\test_file.txt text occured 19 times
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This project is under [MIT](LICENCE) license.