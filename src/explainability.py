import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def get_feature_names(pipeline):
    """
    Attempts to extract feature names from a scikit-learn pipeline.
    This is non-trivial because ColumnTransformer changes names/order.
    """
    # This is a heuristic extraction based on our known structure
    # pipeline = [('feature_engineering', FeatEng), ('preprocessor', ColTrans)]
    
    # 1. Get raw columns (numeric + categorical)
    # We don't have the original df here easily, but we can inspect the transformer
    
    col_trans = pipeline.named_steps['preprocessor']
    
    # Extract feature names from OneHotEncoder
    # We need to know which transformer is which.
    # Transformers: [('num', ...), ('cat', ...)]
    
    feature_names = []
    
    # Check 'num' transformer
    # In standard scaler, names don't change, but we need the input names.
    # We saved them implicitly in the order of columns.
    # This is tricky without the dataframe metadata.
    
    # ALTERNATIVE: Use the model's coefficients directly and just try to map them meaningfully 
    # OR, rely on the fact that we saved X_train_processed.csv which HAS headers!
    
    return feature_names

def generate_explanations(model_dir="models", data_dir="data", output_dir="plots"):
    print("--- Phase 7: Explainability & Insights ---")
    
    model_path = os.path.join(model_dir, "best_model.pkl")
    if not os.path.exists(model_path):
        # Fallback
        model_path = os.path.join("..", model_path)
        data_dir = os.path.join("..", data_dir)
        output_dir = os.path.join("..", output_dir)
    
    model = joblib.load(model_path)
    
    # Load processed training data to get feature names
    X_train = pd.read_csv(os.path.join(data_dir, "X_train_processed.csv"))
    feature_names = X_train.columns.tolist()
    
    importances = None
    
    # Check model type
    if hasattr(model, "coef_"):
        # Linear Regression
        importances = model.coef_
        print("Model: Linear Model (Coefficients extracted)")
    elif hasattr(model, "feature_importances_"):
        # Random Forest / GBM
        importances = model.feature_importances_
        print("Model: Tree Ensemble (Feature Importances extracted)")
    else:
        print("Model structure not supported for direct extraction.")
        return

    # Create DataFrame
    fi_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    })
    
    # For Linear Regression, magnitude matters
    fi_df['Abs_Importance'] = fi_df['Importance'].abs()
    fi_df = fi_df.sort_values(by='Abs_Importance', ascending=False).head(15) # Top 15
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.barplot(x="Importance", y="Feature", data=fi_df, palette="viridis")
    plt.title("Top Feature Drivers of Exam Score")
    plt.xlabel("Impact (Coefficient/Importance)")
    plt.tight_layout()
    
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "feature_importance.png")
    plt.savefig(save_path)
    print(f"Feature importance plot saved to {save_path}")

def get_feature_importance(model_dir="models", data_dir="data"):
    """
    Returns feature importance as a list of dicts for API consumption.
    """
    model_path = os.path.join(model_dir, "best_model.pkl")
    pipeline_path = os.path.join(model_dir, "preprocessing_pipeline.pkl")
    
    # Path fallbacks
    if not os.path.exists(model_path):
        model_path = os.path.join("..", "..", model_dir, "best_model.pkl")
        pipeline_path = os.path.join("..", "..", model_dir, "preprocessing_pipeline.pkl")
        
    if not os.path.exists(model_path) or not os.path.exists(pipeline_path): 
        print("Model or pipeline not found.")
        return []

    model = joblib.load(model_path)
    pipeline = joblib.load(pipeline_path)
    
    feature_names = []
    
    # Try to extract names from ColumnTransformer
    try:
        if hasattr(pipeline, "get_feature_names_out"):
            feature_names = pipeline.get_feature_names_out()
        else:
            # Fallback manual extraction
            # Based on preprocessing.py structure: ['num', 'cat']
            # We know the order: numeric then categorical
            
            # Numeric columns from preprocessing.py
            num_cols = ['age', 'study_hours', 'class_attendance', 'sleep_hours', 'study_efficiency']
            
            # Categorical columns
            cat_cols = ['gender', 'course', 'internet_access', 'sleep_quality', 'study_method', 'facility_rating', 'exam_difficulty']
            
            # Get encoder from transformer
            # Accessing the 'cat' transformer
            # ColumnTransformer.transformers_ is a list of tuples
            # We search for 'cat'
            trans = pipeline.named_steps.get('preprocessor')
            if trans:
                for name, est, cols in trans.transformers_:
                    if name == "num":
                        feature_names.extend(num_cols)
                    elif name == "cat" and hasattr(est, "get_feature_names_out"):
                        feature_names.extend(est.get_feature_names_out(cat_cols))
    except Exception as e:
        print(f"Error extracting names: {e}")
        # Last resort fallback if everything fails
        feature_names = [f"Feature {i}" for i in range(100)] 

    importances = []
    if hasattr(model, "coef_"):
        importances = model.coef_
    elif hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    else:
        return []
        
    # Create list of dicts
    data = []
    for i, imp in enumerate(importances):
        if i < len(feature_names):
            name = str(feature_names[i])
            # Clean up sklearn output like "cat__gender_male" -> "Gender: Male"
            name = name.replace("cat__", "").replace("num__", "")
            name = name.replace("_", " ").title()
            
            data.append({"feature": name, "importance": abs(float(imp))})
        
    # Sort by importance desc
    data.sort(key=lambda x: x['importance'], reverse=True)
    return data[:10] # Top 10


if __name__ == "__main__":
    generate_explanations()
