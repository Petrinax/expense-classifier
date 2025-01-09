from expense_classifier.pipeline import Pipeline

if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.ingest("../datasets/sample_data.csv")
    pipeline.transform()
    pipeline.categorize()
    pipeline.file_correction()
    pipeline.publish_data()
    # pipeline.manual_correction()
    print("Pipeline Completed")
