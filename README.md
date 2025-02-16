# AWS Infrastructure as Code (IaC) for ETL Job on Kindle Store Meta Data

This repository contains an **AWS Infrastructure as Code (IaC)** solution that uses **boto3** to automate the setup of AWS resources and perform an **Extract, Transform, Load (ETL)** job on the `meta_Kindle_Store.jsonl.7z` dataset.

The ETL job processes the nested JSON structure, flattens it, and converts it into a **Parquet format** for further data analysis.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [AWS Resources Setup](#aws-resources-setup)
4. [ETL Job Workflow](#etl-job-workflow)

---

## Overview

This project automates the creation of AWS resources using **boto3**, including:

- **S3**: To store raw data (`meta_Kindle_Store.jsonl.7z`) and processed Parquet files.
- **EC2**: For running lightweight tasks or serving as a bastion host.
- **IAM**: To manage permissions for EMR and other services.
- **EMR**: To process the dataset by flattening the nested JSON structure and converting it into Parquet format.
- **Security Groups**: To ensure secure access to EC2 and EMR clusters.

The ETL job is executed on an **EMR cluster**, which handles the heavy lifting of processing the large `meta_Kindle_Store.jsonl.7z` file.

---

## Prerequisites

Before running this project, ensure you have the following:

- **AWS CLI** installed and configured with appropriate credentials.
- **Python 3.7+** installed.
- **Boto3** library installed (`pip install boto3`).
- An S3 bucket to store the input (`meta_Kindle_Store.jsonl.7z`) and output (Parquet files).
- Basic knowledge of AWS services like S3, EC2, IAM, EMR, and Security Groups.

---

## AWS Resources Setup

The following AWS resources will be created using the provided scripts:

1. **IAM Roles**:
   - IAM roles for EMR and EC2 instances with necessary permissions to access S3 and execute Spark jobs.

2. **S3 Bucket**:
   - Stores the raw `meta_Kindle_Store.jsonl.7z` file.
   - Stores the processed Parquet files after the ETL job.

3. **Security Group**:
   - Configured to allow necessary traffic between EC2, EMR, and other AWS resources.

4. **EC2 Key Pair**:
   - A key pair is created for SSH access to EC2 instances (if needed).

5. **EMR Cluster**:
   - The EMR cluster is responsible for running the ETL job. It processes the `meta_Kindle_Store.jsonl.7z` file by:
     - Flattening the nested JSON structure.
     - Converting the JSON data into Parquet format for efficient querying and analysis.

---

## ETL Job Workflow

The ETL job follows these steps:

1. **Extract**:
   - The `meta_Kindle_Store.jsonl.7z` file is downloaded from the S3 bucket to the EMR cluster.
   
2. **Transform**:
   - The nested JSON structure is flattened using PySpark.
   - The JSON data is converted into Parquet format for better performance in analytical queries.

3. **Load**:
   - The transformed Parquet files are uploaded back to the S3 bucket for further analysis.

