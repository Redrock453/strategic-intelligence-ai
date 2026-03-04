# Guidelines for AI Agents

## Architecture  
The architecture of the AI agents in this project follows a modular design. Each agent is responsible for a specific function and can be developed, tested, and deployed independently. This structure allows for scalability and maintainability.

### Components  
1. **Agent Framework**: A core framework that provides shared functionalities for all agents.
2. **Agent Modules**: Individual modules that implement specific behaviors. Each module should adhere to the interfaces defined by the Agent Framework.

## Coding Standards  
1. **Language and Framework**: Use Python 3.7+ with the following frameworks:
   - TensorFlow or PyTorch for neural networks
   - Flask or FastAPI for creating web interfaces
2. **File Naming**: Use snake_case for files and folders. Any class names should use PascalCase.
3. **Comments and Documentation**: Write descriptive comments and document public methods thoroughly using docstrings.
4. **Code Format**: Use `black` for automatic code formatting and `flake8` for linting.

## Testing Practices  
1. **Unit Testing**: Each agent module must have corresponding unit tests. Use `unittest` or `pytest` for testing.
2. **Test Coverage**: Aim for a minimum of 80% test coverage using coverage.py.
3. **Integration Testing**: Perform integration tests for interactions between multiple agent modules.

## Project-Specific Conventions  
1. **Agent Configurations**: Store configurations for agents in a separate `config.yaml` file. All agents should read their configuration from this file.
2. **Logging**: Use the `logging` module for logging messages. Logs should be categorized into DEBUG, INFO, WARNING, ERROR, and CRITICAL levels.
3. **Version Control**: Follow the Git flow strategy for version control. Always create a new branch for features or bug fixes, and submit a pull request for merging into the main branch.

## Additional Resources  
Refer to the [LangGenius Project Guidelines](https://github.com/langgenius/dify/AGENTS.md) for further insights.