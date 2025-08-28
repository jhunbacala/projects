# Adding a new AWS CLI Profile

You can add additional AWS credentials by creating a new AWS CLI profile. Here are the steps:

1.  **Open your terminal.**
2.  **Run the `aws configure` command with the `--profile` flag, specifying a name for your new profile.** For example, if you want to name your new profile `work-account`, you would run:

    ```bash
    aws configure --profile work-account
    ```
3.  **You will be prompted to enter your AWS credentials and a default region.**
    *   `AWS Access Key ID`: Enter the access key for your new credentials.
    *   `AWS Secret Access Key`: Enter the secret key for your new credentials.
    *   `Default region name`: Enter the AWS region you want to use with this profile (e.g., `us-east-1`).
    *   `Default output format`: You can leave this blank or specify a format like `json`.

Once you've completed these steps, your new credentials will be stored in a new profile.

To use your new profile for an AWS command, you can use the `--profile` flag. For example, to list your S3 buckets using your `work-account` profile, you would run:

```bash
aws s3 ls --profile work-account
```

Your AWS credentials are now stored in the `~/.aws/credentials` file.

## Listing Your AWS CLI Profiles

To see a list of all the profiles you have configured, you can use the `list-profiles` command:

```bash
aws configure list-profiles
```

This will output a list of all profile names from your AWS credentials and config files.
