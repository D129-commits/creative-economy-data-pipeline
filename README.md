# Global Creative Economy Data Pipeline

## Project overview

This project demonstrates a reproducible cross-country
economic data workflow using Python, GitHub and AWS S3.



## Data source

World Bank Indicators API.

## Coverage

- 20 economies
- 2015–2023
- Cross-country panel data

## Indicators

The current version includes:

- Internet users (% of population)
- ICT service exports
- Tertiary school enrolment
- GDP per capita

## Workflow

World Bank API  
→ Raw data  
→ Data processing  
→ Automated quality checks  
→ Composite indicator  
→ AWS S3  
→ Dashboard

## Data quality checks

The pipeline automatically evaluates:

- duplicate observations
- missing values
- country coverage
- year coverage

## Composite indicator

The project constructs an illustrative
Digital and Creative Economy Readiness Index.


## Technology

- Python
- Pandas
- World Bank API
- Git
- GitHub
- AWS S3