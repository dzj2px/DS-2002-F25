.PHONY: all fetch analyze clean

# default target
all: analyze

fetch:
	@echo fetching metar data into raw_metars.
	@./fetch_metars.sh
	@echo fetch done.

analyze: fetch
	@echo analyzing json into weather_report.csv
	@./analyze_data.sh
	@echo analyze done. pipeline complete.

clean:
	@echo removing generated files.
	@rm -rf raw_metars weather_report.csv
	@echo clean done.
