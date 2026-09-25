# 📊 Data

This directory contains documentation related to the external datasets used in the Flight Delay Analytics project.

The project uses flight operational data as its primary dataset and historical weather data as an additional external source.

---

## 📁 Data Sources

### 1. BTS Flight Data

The primary dataset contains flight-level operational information used for the analytical model.

The dataset includes information related to:

- Flight dates
- Reporting airlines
- Flight numbers
- Origin and destination airports
- Scheduled and actual departure/arrival times
- Departure and arrival delays
- Cancellations
- Diversions
- Flight distance
- Delay categories

The original dataset contains additional attributes that were not required for the final analytical model.

### Data Processing

The raw flight data was ingested into Microsoft Fabric and transformed using PySpark.

The transformation process included:

```text
Raw BTS Dataset
      ↓
OneLake
      ↓
PySpark
      ↓
Column Selection
      ↓
Data Quality Checks
      ↓
Missing-Value Handling
      ↓
Silver Flight Data
```
The resulting cleaned dataset is represented in the Fabric environment as:

```
silver_flights
```

---

## 2. OpenFlights Airport Reference Data
OpenFlights airport reference data was used to provide airport metadata required for geographic processing.

Relevant attributes include:

- Airport identifier
- Airport name
- City
- Country
- IATA code
- ICAO code
- Latitude
- Longitude
The airport coordinates are particularly important for the weather-data integration because the weather API requires geographic coordinates.

### Airport Mapping
The flight dataset contains BTS airport identifiers and airport IATA codes.

The OpenFlights data provides its own airport identifier, so the OpenFlights airport ID is not treated as equivalent to the BTS airport ID.

The mapping is instead based on the airport's IATA code:

```
BTS Flight Data
      │
      │ Origin / Destination IATA
      ▼
OpenFlights
      │
      ├── Latitude
      └── Longitude
      │
      ▼
Weather API
```

---

## 3. Historical Weather Data
Historical weather data was obtained through the Open-Meteo Historical Weather API.

The weather data provides environmental conditions that can be analyzed alongside flight operations.

Relevant variables include:

- Temperature
- Precipitation
- Cloud cover
- Wind speed
- Weather code
The weather data is associated with airport location and time so that weather conditions can be compared with flight operations.

```
Airport
   │
   ├── Latitude
   └── Longitude
          │
          ▼
   Open-Meteo API
          │
          ▼
 Historical Weather
          │
          ▼
Weather Analysis
```

---

# 🔄 Data Flow
The datasets are combined through the following workflow:

```
                 BTS Flight Data
                       │
                       ▼
                    OneLake
                       │
                       ▼
                 PySpark Cleaning
                       │
                       ▼
                  Silver Layer
                       │
                       ├───────────────┐
                       │               │
                       ▼               ▼
               Airport Mapping    Weather API
                       │               │
                       └───────┬───────┘
                               ▼
                       Analytical Model
                               │
                               ▼
                           Power BI
```

---

# 🧹 Data Quality
Data quality checks were performed during the transformation stage.

The checks included:

- Null-value analysis
- Column selection
- Data type inspection
- Identification of fields with expected missing values
- Removal of records with missing values in required flight attributes
Some attributes naturally contain missing values.

For example, delay-cause fields may be unavailable for flights where the corresponding delay category does not apply. These fields were therefore treated differently from required flight attributes.

---

# 📦 Data Availability
The raw datasets are not stored directly in this repository.

This repository contains the documentation and transformation/modeling artifacts rather than copies of potentially large external datasets.

To reproduce the project:

1. Obtain the BTS flight dataset.
2. Obtain the OpenFlights airport reference data.
3. Load the datasets into the Microsoft Fabric workspace.
4. Run the transformation notebooks.
5. Retrieve historical weather data through the Open-Meteo API.
6. Continue through the dimensional modeling and reporting layers.

---

# 🔗 External Sources

- Bureau of Transportation Statistics (BTS) — Flight operational data
- OpenFlights — Airport reference data
- Open-Meteo — Historical weather API
See the main project README for the complete architecture and implementation details.

---

## ⚠️ Important Notes

- The raw datasets are treated as external source data.
- OpenFlights airport IDs and BTS airport IDs are different identifier systems.
- Airport IATA codes are used as the mapping attribute between the flight data and airport reference data.
- Weather data is used to investigate relationships between environmental conditions and flight operations; the project does not establish causal relationships.
