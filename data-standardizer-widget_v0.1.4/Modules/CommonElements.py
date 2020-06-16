# default configurations


# Display Configuration
des_style = {'description_width': 'initial'}
text_font_color = 'black'
text_font_style = ''
output_layout = {'border': '2px solid black'}

active_button_color = "lightgreen"
inactive_button_color = "orange"
theme_color = "lightblue"

# Error Messages
train_data_err = "Training data not selected"
dep_var_err = "Dependent variable not specified"
dep_var_id_match_err = "Dependent variable and Index column cannot be same"
generic_error = "Something went wrong !!!"

# Keys
LR_KEY = "Linear"
RIDGE_KEY = "Ridge"
LASSO_KEY = "Lasso"
ELASTICNET_KEY = "ElasticNet"
MSE_KEY = "Mean Sq Error"
MAE_KEY = "Mean Abs Error"
MedAE = "Median Abs Error"
EVAR_KEY = "Explained Variance"
R2_KEY = "R Squared"
test_output_file_name = "predictions_test_data.csv"
train_output_file_name = "predictions_train_data.csv"
summary_output_file_name = "model_summary.txt"
model_pkl_name = "model_object.pkl"

# Default values
normalize_default = False
fit_intercept_default = True
alpha_default = 1.0
l1_ratio_default = 0.5
