import argparse
import sys
from loguru import logger

from olist_ecommerce.pipeline.data_ingestion.master_table import run_data_pipeline
from olist_ecommerce.pipeline.cleaning.cleaning import run_cleaning_pipeline
from olist_ecommerce.pipeline.feature_engineering.feature import run_feature_pipeline
from olist_ecommerce.modeling.train import train_model
from olist_ecommerce.modeling.predict import predict_segment

logger.remove()
logger.add(sys.stderr, format="{time} | {level} | {message}")


def run_full():
    logger.info("🚀 Running Full Pipeline")

    run_data_pipeline()
    run_cleaning_pipeline()
    run_feature_pipeline()
    train_model()

    logger.success("✅ Full pipeline completed")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", required=True,
                        choices=["all", "data", "clean", "feature", "train", "predict"])

    parser.add_argument("--category", type=str)
    parser.add_argument("--state", type=str)

    args = parser.parse_args()

    if args.mode == "all":
        run_full()

    elif args.mode == "data":
        run_data_pipeline()

    elif args.mode == "clean":
        run_cleaning_pipeline()

    elif args.mode == "feature":
        run_feature_pipeline()

    elif args.mode == "train":
        train_model()

    elif args.mode == "predict":
        if not args.category or not args.state:
            logger.error("Provide --category and --state")
            sys.exit(1)

        from olist_ecommerce.modeling.predict import predict_segment

        result = predict_segment(args.category, args.state)

        if result is not None:
            print(result)


if __name__ == "__main__":
    main()


#------------- Run Model -------------------------
#  python -m olist_ecommerce.runpipeline --mode all
#  python -m olist_ecommerce.runpipeline --mode train
#  python -m olist_ecommerce.runpipeline --mode clean    
#  python -m olist_ecommerce.runpipeline --mode predict --category "health_beauty" --state "SP"