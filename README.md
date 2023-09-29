# MagicCommits

A Git commit message generator powered by AI. Never struggle with commit messages again.

<img src="https://img.shields.io/pypi/v/magiccommits?color=%2334D058" />
<img src="https://img.shields.io/pypi/pyversions/magiccommits?color=%2334D058" />
<img src="https://img.shields.io/pypi/l/magiccommits?color=%2334D058" />

---

## Installation

Before you start using MagicCommits, make sure you have Python and pip installed. Then, you can install MagicCommits using pip:

```sh
pip install magiccommits
```

If you are using python3 then 
```sh
pip3 install magiccommits
```
Before you can use MagicCommits, you'll need to configure it with your OpenAI API key. If you haven't already, you can retrieve your API key from [OpenAI](https://platform.openai.com/account/api-keys) (Note: You may need to create an account and set up billing).

**Set the OPENAI_KEY**
 ```bash
    mc config set OPENAI_KEY=<your-token>
```

## Usage
Execute `magiccommits or mc` to generate the commit messages


## Additional Options

|  | Command            | Example                                       | Functionality                                 |
|-------|--------------------|-----------------------------------------------|-----------------------------------------------|
| 1     | `-t` or `--ticket` | `mc -t PROJ-123`          | Set the ticket number for your commit message |
| 2     | `-a` or `--add`    | `mc -a`             | Perform a `git add .` operation before commit |
| 3     | `-u` or `--update` | `mc commit -u`        | Perform a `git add --update` operation        |

- Command: Specifies the command or option to use.
- Example: Provides an example usage of the option in a command.
- Functionality: Describes the functionality or purpose of the option.

You can use these additional options to customize your commit messages and perform relevant Git operations as needed in your project workflow.


## Configuration

You can use these keys to configure various aspects of the project. To set the value for a key, you must use the format `key=value` when using the `mc config set` command. To retrieve the values for these keys, you can use the `mc config get` command, either for all values or a specific key.

## Configuration Keys

### `OPENAI_KEY [Required]`

- **Description:** This key is used to specify the OpenAI API key.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set OPENAI_KEY=sk-test
    ```
  - To retrieve the value:
    ```bash
    mc config get OPENAI_KEY
    ```

### `locale [OPT]`

- **Description:** This key defines the locale or language for text generation.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set locale=en
    ```
  - To retrieve the value:
    ```bash
    mc config get locale
    ```

### `generate [OPT]`

- **Description:** This key determines the number of commit message to generate.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set generate=4
    ```
  - To retrieve the value:
    ```bash
    mc config get generate
    ```

### `type [OPT]`

- **Description:** This key specifies the type of commit generation.

- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set type=conventional
    ```
  - To retrieve the value:
    ```bash
    mc config get type
    ```

#### `conventional`

- **Explanation:** Generates commit messages following the conventional commit format.

- **Example:** 
  - Commit Message: `feat: add new feature`
  - Description: A conventional commit format with a type ("feat" for feature) and a brief description.

#### `conventional-emoji`

- **Explanation:** Generates commit messages following the conventional commit format with added emojis.

- **Example:** 
  - Commit Message: `feat: add new feature :sparkles:`
  - Description: A conventional commit format with an emoji (:sparkles:) for visual appeal and a type ("feat") with a brief description.

#### `message`

- **Explanation:** Generates simple and concise commit messages.

- **Example:** 
  - Commit Message: `Update README.md`
  - Description: A straightforward commit message with a focus on the action ("Update README.md").

#### `message-emoji`

- **Explanation:** Generates simple commit messages with added emojis.

- **Example:** 
  - Commit Message: `Fix a critical bug :bug:`
  - Description: A simple commit message with an emoji (:bug:) for visual context, describing the action ("Fix a critical bug").


### `proxy [OPT]`

- **Description:** This key allows you to set a proxy server for network requests.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set proxy=http
    ```
  - To retrieve the value:
    ```bash
    mc config get proxy
    ```

### `model [OPT]`

- **Description:** This key defines the model to be used for commit generation.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set model=gpt-3.5-turbo
    ```
  - To retrieve the value:
    ```bash
    mc config get model
    ```

### `timeout [OPT]`

- **Description:** This key sets the maximum timeout (in milliseconds) for API requests.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set timeout=10000
    ```
  - To retrieve the value:
    ```bash
    mc config get timeout
    ```

### `max_length [OPT]`

- **Description:** This key specifies the maximum length of generated text.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set max_length=50
    ```
  - To retrieve the value:
    ```bash
    mc config get max_length
    ```

### `max_token [OPT]`

- **Description:** This key determines the maximum number of tokens in the generated text.
- **Example Setting:** 
  - To set the value:
    ```bash
    mc config set max_token=200
    ```
  - To retrieve the value:
    ```bash
    mc config get max_token
    ```

### `copy_commit [OPT]`

- **Description:** This key is a boolean flag that determines whether to copy the generated text to the clipboard.
- **Example Setting (True):** 
  - To set the value:
    ```bash
    mc config set copy_commit=True
    ```
  - To retrieve the value:
    ```bash
    mc config get copy_commit
    ```

## Getting Configuration Values

To retrieve the values for these configuration keys, you can use the following commands:

- To get all configuration values:

```bash
mc config get
```

## Usage

### Generate Commit Messages

You can use MagicCommits to effortlessly generate commit messages for your staged changes:


MagicCommits will analyze your Git diff and employ AI to suggest a commit message. You can then choose to commit, commit and push, or copy the message to your clipboard.

### Version

To check the current version of MagicCommits, you can use the following command:

```sh
mc --version
```

## Credits

MagicCommits is inspired by [AI Commits](https://github.com/Nutlope/aicommits), created by [Hassan El Mghari](https://github.com/Nutlope).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center" style="padding: 10px;">
  <strong>Made in Nepal</strong> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Flag_of_Nepal.svg/20px-Flag_of_Nepal.svg.png" alt="Nepal Flag">
</div>
