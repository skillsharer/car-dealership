# Car Dealership ML Train Experiments:

## ML part of the task:

```
You are working as a professional IT consultant for a company selling second-hand cars. The company would like to improve its internal services by using a model to estimate the potential selling price of the car in advance. They request you to implement a solution using AWS services. The company provides data on its previous sales (sample_input.csv). This dataset includes attributes of the car, the customer, the dealership, etc.

They want you to create a notebook that takes the data from the curated zone, trains a model of your choice, and evaluates it. Since the company wants to sell its current inventory as soon as possible, they would prefer a model that slightly underestimates the price. You might use an sklearn compatible framework to implement your model.
```

## Steps what I was taking:
- Data cleansing: 
    - Removed carnames which were missing.
    - Kept only these features: ```SELECTED_FEATURES = [
    "carname",
    "fueltype",
    "aspiration",
    "doornumber",
    "carbody",
    "drivewheel",
    "enginelocation",
    "wheelbase",
    "color",
    "carlength",
    "carwidth",
    "carheight",
    "curbweight",
    "cylindernumber",
    "enginesize",
    "compressionratio",
    "horsepower",
    "peakrpm",
    "citympg",
    "highwaympg",
    "price",
]```
    - carname contained subtype, so I just kept the manufacturer.
    - carname also had typos. I mapped the typos onto real manufacturer.
    - Split the data into train and test set (80%-20%). And separated independent variables to dependent variable (price).
    - Imputed the train and test sets using mode and mean.
    - Scaled the features with z-score scale.
    - One-hot-encoded those features which was truly categorical.

    This resulted the following train columns:
        ```
        ['wheelbase', 
        'carlength', 
        'carwidth', 
        'carheight', 
        'curbweight',
        'cylindernumber', 
        'enginesize', 
        'compressionratio', 
        'horsepower',
        'peakrpm', 
        'citympg', 
        'highwaympg', 
        'carname_audi', 
        'carname_bmw',
        'carname_buick', 
        'carname_chevrolet', 
        'carname_dodge', 
        'carname_honda',
        'carname_isuzu', 
        'carname_jaguar', 
        'carname_mazda', 
        'carname_mercury',
        'carname_mitsubishi', 
        'carname_nissan', 
        'carname_peugeot',
        'carname_plymouth', 
        'carname_porsche', 
        'carname_renault',
        'carname_saab', 
        'carname_subaru', 
        'carname_toyota',
        'carname_volkswagen', 
        'carname_volvo', 
        'fueltype_gas',
        'aspiration_turbo', 
        'doornumber_two', 
        'carbody_hardtop',
        'carbody_hatchback', 
        'carbody_sedan', 
        'carbody_wagon', 
        'drivewheel_fwd',
        'drivewheel_rwd', 
        'enginelocation_rear', 
        'color_black', 
        'color_blue',
        'color_fuchsia', 
        'color_gray', 
        'color_green', 
        'color_lime',
        'color_maroon', 
        'color_navy', 
        'color_olive', 
        'color_purple',
        'color_silver', 
        'color_teal', 
        'color_white', 
        'color_yellow']
        ```

- Data explore phase showed me that multiple features show monotonic relationships with price which tells us that linear regression is good for a baseline. To make better assumptions about these relationships, residual plots can help after training. 

- Train experiments:
  1. Simple linear regression:
  ```
    Train set performance: 

    Mean Absolute Error (MAE): 1146.82
    Mean Squared Error (MSE): 2399665.33
    Root Mean Squared Error (RMSE): 1549.09
    R-squared (R2) Score: 0.95

    Test set performance: 

    Mean Absolute Error (MAE): 1814.19
    Mean Squared Error (MSE): 10332477.97
    Root Mean Squared Error (RMSE): 3214.42
    R-squared (R2) Score: 0.89
  ```
  2. Log scale the price:
  ```
    Train set performance: 

    Mean Absolute Error (MAE): 1070.40
    Mean Squared Error (MSE): 2737537.21
    Root Mean Squared Error (RMSE): 1654.55
    R-squared (R2) Score: 0.94

    Test set performance: 

    Mean Absolute Error (MAE): 1795.85
    Mean Squared Error (MSE): 6459825.86
    Root Mean Squared Error (RMSE): 2541.62
    R-squared (R2) Score: 0.93
  ```
  3. Ridge with different alphas (test set only):
  ```
    alpha: 0.1
    Mean Absolute Error (MAE): 1802.87
    Mean Squared Error (MSE): 10201148.78
    Root Mean Squared Error (RMSE): 3193.92
    R-squared (R2) Score: 0.89

    alpha: 1
    Mean Absolute Error (MAE): 1894.50
    Mean Squared Error (MSE): 10529785.23
    Root Mean Squared Error (RMSE): 3244.96
    R-squared (R2) Score: 0.89

    alpha: 5
    Mean Absolute Error (MAE): 2127.94
    Mean Squared Error (MSE): 12868535.83
    Root Mean Squared Error (RMSE): 3587.27
    R-squared (R2) Score: 0.86

    alpha: 10
    Mean Absolute Error (MAE): 2275.26
    Mean Squared Error (MSE): 14375399.08
    Root Mean Squared Error (RMSE): 3791.49
    R-squared (R2) Score: 0.85

    alpha: 20
    Mean Absolute Error (MAE): 2388.64
    Mean Squared Error (MSE): 16004538.99
    Root Mean Squared Error (RMSE): 4000.57
    R-squared (R2) Score: 0.83

    alpha: 50
    Mean Absolute Error (MAE): 2508.03
    Mean Squared Error (MSE): 18449738.64
    Root Mean Squared Error (RMSE): 4295.32
    R-squared (R2) Score: 0.81

    alpha: 100
    Mean Absolute Error (MAE): 2621.63
    Mean Squared Error (MSE): 20987093.14
    Root Mean Squared Error (RMSE): 4581.17
    R-squared (R2) Score: 0.78
    ```
4. Feature engineering:

    ```
    Engineered Linear Model - Train set performance:

    Mean Absolute Error (MAE): 1058.87
    Mean Squared Error (MSE): 1903340.80
    Root Mean Squared Error (RMSE): 1379.62
    R-squared (R2) Score: 0.96

    Engineered Linear Model - Test set performance:

    Mean Absolute Error (MAE): 1854.01
    Mean Squared Error (MSE): 10341840.66
    Root Mean Squared Error (RMSE): 3215.87
    R-squared (R2) Score: 0.89
    ```

## Possible next steps:

The baseline performs reasonably on the test set. However, we possibly see overfitting on the train set (especially when I added engineered features) and also huge errors especially when prices are higher. Currently I just multiplied the model output by 0.95 to 'slightly underestimate' the price as it was in the task requirements, however it is not a robust solution. A better solution would be Quantile Regression, where we can train a lower percentile model (e.g. 45th percentile).

- Feature engineering: Production year would help a lot I think, which will tells us the age of the car at the time of the sale. Also, mileage would help too, because these two features have a huge effect on the used car prices. I was thinking about to engineer a feature which would make assumption of the vehicle age (based on model production year range and sale date), but my time was limited.

- Additional data collection: To avoid overfitting, additional data gathering also could help.

- Make modular and reusable training pipeline, because ipynbs hard to maintain.

- Experiment with Quantile Regression and Tree based methods. 

## Notes:

The whole project implementation with the experiments took me around 24 hours. 
