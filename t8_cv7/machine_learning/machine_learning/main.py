from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from machine_learning.data_handling import Dataset
from machine_learning.experiment import Experiment
from machine_learning.result_plots import Plotter


def main():
    """
    Main function to execute the model training and evaluation pipeline.

    Initializes the dataset, defines models and their parameter grids,
    and invokes the replication of model training and evaluation.
    """
    # Initialize dataset and preprocess the data
    dataset = Dataset()

    # Define models to be trained
    models = {
        "Logistic Regression": LogisticRegression(solver='liblinear'),  # Solver specified for clarity
        "Tree Classifier": DecisionTreeClassifier()
    }

    # Define hyperparameter grids for tuning
    param_grids = {
        "Logistic Regression": {"C": [0.1, 1, 10], "max_iter": [10000]},
        "Tree Classifier": {"max_depth": [1, 3, 5], "min_samples_leaf": [1]},
    }

    experiment = Experiment(models, param_grids, n_replications=10)
    results = experiment.run(dataset.data, dataset.target)

    # Plot the results using the Plotter class
    plotter = Plotter()
    plotter.plot_metric_density(results, metrics=('accuracy', 'roc_auc', 'f1_score', 'precision'))
    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['accuracy'].apply(list).to_dict(),
        'Accuracy per Replication and Average Accuracy', 'Accuracy')
    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['f1_score'].apply(list).to_dict(),
        'F1 Score per Replication and Average F1 Score', 'F1 Score')
    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['precision'].apply(list).to_dict(),
        'Precision per Replication and Average Precision Score', 'Precision')
    plotter.plot_evaluation_metric_over_replications(
        experiment.results.groupby('model')['precision'].apply(list).to_dict(),
        'Cohen Kappa per Replication and Average Cohen Kappa Score', 'Cohen Kappa')
    plotter.plot_confusion_matrices(experiment.mean_conf_matrices)
    plotter.print_best_parameters(results)


if __name__ == "__main__":
    main()
