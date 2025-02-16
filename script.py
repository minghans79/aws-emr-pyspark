from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys

if __name__ == "__main__":
    spark = SparkSession.builder.appName("script").getOrCreate()
    spark.conf.set('spark.sql.caseSensitive', True)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    df = spark.read.json(input_path)

    #flatten author
    df = df.withColumn(
        'author_name', 
        df['author.name']).withColumn('author_avatar', 
        df['author.avatar']).withColumn('author_about', 
        explode(df['author.about'])).drop('author')

    #flatten categories
    df = df.withColumn('categories',explode(df['categories']))

    #flatten description
    df = df.withColumn('description',explode(df['description']))

    #flatten details
    df = df.select(
        "*",  # Select all top-level columns
        col("details.`11 99`").alias("details_11_99"),
        col("details.`12 99`").alias("details_12_99"),
        col("details.`13 67`").alias("details_13_67"),
        col("details.`Country of Origin`").alias("details_country_of_origin"),
        col("details.`Date First Available`").alias("details_date_first_available"),
        col("details.Dimensions").alias("details_dimensions"),
        col("details.`Domestic Shipping`").alias("details_domestic_shipping"),
        col("details.`Enhanced typesetting`").alias("details_enhanced_typesetting"),
        col("details.`File Size`").alias("details_file_size"),
        col("details.`File size`").alias("details_file_size_duplicate"),  # Handle duplicate column
        col("details.Hardcover").alias("details_hardcover"),
        col("details.`ISBN 10`").alias("details_isbn_10"),
        col("details.`International Shipping`").alias("details_international_shipping"),
        col("details.`Is Discontinued By Manufacturer`").alias("details_is_discontinued"),
        col("details.`Item Weight`").alias("details_item_weight"),
        col("details.`Item model number`").alias("details_item_model_number"),
        col("details.Language").alias("details_language"),
        col("details.Manufacturer").alias("details_manufacturer"),
        col("details.`Manufacturer recommended age`").alias("details_manufacturer_recommended_age"),
        col("details.`On page writing`").alias("details_on_page_writing"),
        col("details.`Package Dimensions`").alias("details_package_dimensions"),
        col("details.`Page numbers source ISBN`").alias("details_page_numbers_source_isbn"),
        col("details.`Print length`").alias("details_print_length"),
        col("details.`Product Bundle`").alias("details_product_bundle"),
        col("details.`Product Dimensions`").alias("details_product_dimensions"),
        col("details.`Publication date`").alias("details_publication_date"),
        col("details.Publisher").alias("details_publisher"),
        col("details.`Screen Reader`").alias("details_screen_reader"),
        col("details.`Simultaneous device usage`").alias("details_simultaneous_device_usage"),
        col("details.`Sticky notes`").alias("details_sticky_notes"),
        col("details.`Text to Speech`").alias("details_text_to_speech"),
        col("details.`Word Wise`").alias("details_word_wise"),
        col("details.`X Ray`").alias("details_x_ray"),
        col("details.`X Ray for textbooks`").alias("details_x_ray_for_textbooks")
    ).drop('details')

    df = df.select(
        '*',
        explode('videos').alias('video')
        ).select('*',
            col('video.title').alias('video_title'),
            col('video.url').alias('video_url'),
            col('video.user_id').alias('video_user_id')).drop('videos')

    df = df.drop('video')

    df = df.select(
        "*",  # Keep all other columns
        explode("images").alias("image")  # Explode the array into rows
    ).select(
        "*",  # Keep all existing columns
        col("image.hi_res").alias("image_hi_res"),   # Extract and rename 'hi_res'
        col("image.large").alias("image_large"),     # Extract and rename 'large'
        col("image.thumb").alias("image_thumb"),     # Extract and rename 'thumb'
        col("image.variant").alias("image_variant")  # Extract and rename 'variant'
    ).drop("images")  # Drop the intermediate 'image' column

    df = df.drop('image')

    df = df.withColumn('features', explode('features'))

    #partitioning for more efficient quering 
    #using zstd compression for better performance
    df.write.mode("overwrite").partitionBy("main_category").option("compression", "zstd").parquet(output_path)  

    spark.stop()