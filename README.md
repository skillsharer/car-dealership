# Car Dealership Exercise

## Goal of the project:
This exercise is about an imaginary car dealership company which wants to estimate vehicle prices across different types of cars.
They want to use ML algorithms for price prediction and AWS services for data preprocessing and deletion based on unimportant columns and missing rows. For the ML part, they want a slightly underestimating price predictor.

## Quick start:
Train a basic car price estimator using preprocessing AWS lambda function.

1. Prerequisites:  
    - uv
    - AWS account with permissions for S3, Lambda, IAM
    - AWS CLI configured
    - Terraform installed
    - .env vars filled out

    See details below in the document.

2. Exact order of commands:
    - `uv venv .venv`
    - `source .venv/bin/activate`
    - `uv sync --extra train`
    - `./scripts/build_lambda.sh`
    - `cd terraform`
    - `terraform init`
    - `terraform apply`
    - `LANDING_BUCKET=$(terraform output -raw landing_bucket_name) CURATED_BUCKET=$(terraform output -raw curated_bucket_name)`
    - `cd ..`
    - `aws s3 cp ./data/input.csv "s3://$LANDING_BUCKET/sample_input.csv"`
    - `aws s3 ls "s3://$CURATED_BUCKET/curated/"` - Verify file appears in curated bucket
    - `aws s3 cp "s3://$CURATED_BUCKET/curated/sample_input.csv" ./model/processed_output.csv`
    - Use `model/train.ipynb` to train ML model.
    - (`terraform destroy` - do not forget to remove the `.csv` files first from the bucket.)


## Repo design and help for the review:
The project is built up under different subdirectories. Let's see them one-by-one:
- `./data` directory contains my data exploration functions and plots in the `explore.ipynb`. This state is where I started the project. I did not provide here the original data, but that `input.csv` is that which I worked on in the early stage. 
  - Results of this stage: 
    - I reviewed features one-by-one, 
    - Plotted feature histograms, 
    - Compared features to each other,
    - Found missing data and tried out multiple imputation techniques
    - Tried out different scaling methods

I went back to this stage multiple times, because in the training phase many new findings emerged and needed to improve my data cleansing methods.

- `./model` directory contains my ML model training experiments. The notebook contains the necessary data handling methods, along with the training and evaluation of the model. I have 4 experiments in the notebook to try out different methods to improve the model performance. See details [here](./model/README.md).

- `./scripts`, `terraform` and `src`: These are those directories which responsible for the `AWS` data preprocessing infrastructure. `./scripts/build_lambda.sh` is my local build script which creates a `.zip` file under the `dist` directory for the lambda service. For the infrastructure blueprint, I required to use terraform, therefore those files take place in `terraform` folder. `src` is the heart of the service, where lambda function and the helper functions take place.

## Design considerations:
I used `.ipynb` for data and ML training experiments. This was handy for fast try outs and reusability, but in a real production environment it is hard to maintain, hard to review. I do not wanted to upload `.csv` files to git, I always handle them separately from projects to never expose any private information. 

By the way, at the current project state the landing bucket purely gets the private information which is also not good. In a real production environment we shall hide those information. The terraform files create two `S3` buckets (LANDING and CURATED) and a `lambda` function which loads the `.csv` from the landing zone, then deletes the missing rows and not required columns from the data, then puts the cleaned file to the curated zone. For the lambda function, I needed to create a `bash` script to build and pack together the necessary packages. I could use Dockerfile as well, but I wanted to keep lightweight the project. Additionally, in `AWS`, I created a sub user to avoid root user usage and follow least privilege principles.  

For the ML part I wanted to start with the simplest linear regression model and experiment iteratively. I put here the further data imputation and conversion methods, because both the task said that lambda is only for deletion and my consideration is aligned as well, because heavy data processing shall be done elsewhere in the pipeline not in `lambda`.

I used `uv` for python module management, that was relied purely only my preference.

## How to use what:

### Local experiments:

1. First, install `uv` at [here](https://docs.astral.sh/uv/getting-started/installation/).
2. Create a virtual environment with `uv venv .venv`.
3. Then activate: `source .venv/bin/activate`
4. Then, `uv sync --extra train` to install the extra dependencies for both `.ipynb` files.

To try out and reproduce my data experiments, put the original `.csv` into the `./data` folder and rename it `input.csv`, or give the path for the csv loader inside the notebook.

### For lambda deployment and usage:

AWS CLI configure:
1. `aws configure --profile your-profile-name`
2. Then fill out the necessary keys.
3. Then `export AWS_PROFILE=your-profile-name`
4. Try out: `aws sts get-caller-identity` or `aws sts get-caller-identity --profile your-profile-name`. This returns your current account info.

Also, install terraform from [here](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).

Create a `.env` file based on the `.env.example` and fill out the necessary project variables which terraform can use.

S3 bucket names implicitly created from those variables. First a name prefix:
`name_prefix = "${var.project_name}-${var.environment}-${random_id.suffix.hex}"` which then used for the bucket creation:

```
resource "aws_s3_bucket" "landing" {
  bucket = "${local.name_prefix}-landing"
}

resource "aws_s3_bucket" "curated" {
  bucket = "${local.name_prefix}-curated"
}
```

Deployment steps:

1. Build and create a package for lambda: `./scripts/build_lambda.sh`
2. `cd terraform`
3. If you first use terraform, then `terraform init`
4. then `terraform apply`
5. Do not forget to use `terraform destroy` at the end of the review.

Trying out a `.csv` preprocess:

1. Obtain bucket names:
```
LANDING_BUCKET=$(terraform output -raw landing_bucket_name)
CURATED_BUCKET=$(terraform output -raw curated_bucket_name)
```
2. Upload original data: `aws s3 cp ./data/input.csv "s3://$LANDING_BUCKET/sample_input.csv"`
3. Check, whether data processing is finished or not: `aws s3 ls "s3://$CURATED_BUCKET/curated/"`
4. Download processed data: `aws s3 cp "s3://$CURATED_BUCKET/curated/sample_input.csv" ./model/processed_output.csv`

ML train:

The notebook requires a `processed_output.csv` inside that directory to obtain the data. Of course, you can use your own path too.
For my research experiences and thoughts, see the [readme](./model/README.md) under `model` directory.

## AI USAGE STATEMENT:

I used a generative AI-based tool to complete the homework. 

1. I never had experience about terraform, therefore I used to get to know the usage, generate terraform files and get to know the commands. Additionally, I also used a generated lambda function skeleton and bash build script.

2. I used AI for brainstorming further ideas after the first two ML train experiments.

## Thank you
Thank you for reading this readme and taking your time and review this project. Any feedback is really appreciated!