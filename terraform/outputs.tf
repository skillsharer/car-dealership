output "landing_bucket_name" {
  value = aws_s3_bucket.landing.bucket
}

output "curated_bucket_name" {
  value = aws_s3_bucket.curated.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.preprocess.function_name
}