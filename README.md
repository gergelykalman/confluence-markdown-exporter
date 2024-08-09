# Confluence to Markdown Exporter

A simple tool to export Confluence pages to Markdown format. **Note:** This code is not written with security in mind. Do **not** run it on a repository that can contain malicious page titles.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/josh-abram/confluence-markdown-exporter.git
   cd confluence-markdown-exporter
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```sh
python3 confluence-markdown-export.py <url> <username> <token> <out_dir> [--space <space>] [--skip-attachments] [--no-fetch]
```

### Arguments

- **url**: The URL of the Confluence instance (e.g., `https://YOUR_PROJECT.atlassian.net`).
- **username**: Your Confluence username.
- **token**: Your Confluence API token.
- **out_dir**: The directory to output the files to.

### Optional Arguments

- **--space**: Specify the space key to export. If not provided, all spaces will be exported.
- **--skip-attachments**: Skip fetching attachments.
- **--no-fetch**: Only run the Markdown conversion without fetching data from Confluence.

### Example

```sh
python3 confluence-markdown-export.py https://YOUR_PROJECT.atlassian.net your_username your_api_token ./output_dir --space DOCS --skip-attachments
```

## Generating an API Token

1. Go to your Confluence profile.
2. Navigate to **Security**.
3. Under **API Tokens**, click **Manage API Tokens**.
4. Generate a new token and use it as the `token` argument.

## Notes

- The script currently supports single-threaded operation, which is safe for higher chunk sizes during downloads.
- Ensure you have the necessary permissions to access the Confluence instance and export data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
