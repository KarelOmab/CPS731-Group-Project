
# Python Programming Challenge Platform

## Problem Statement
In the fast-paced world of technology, learners from all levels need a secure, user-friendly platform for practicing python programming with real-time feedback. This platform aims to cater to that demand, offering a rich interactive experience for both beginners and experienced developers.

## Platform Overview (Non-technical)
The platform presents a web-based coding practice area where users are greeted with a variety of coding challenges. Users can engage with challenges, write or paste their code in an embedded coding environment, and receive immediate feedback upon submission.

## Goals
- **Interactive Learning**: To provide an interactive web-based platform full of diverse coding challenges.
- **Content Management**: Enable moderators to manage programming challenges effectively.
- **Real-time Feedback**: Instant feedback on user submissions with execution details.
- **Secure Execution**: Ensure all code is executed safely, protecting the platform's integrity.
- **Extensibility**: Maintain a system where new challenges can be introduced smoothly.

## Functional Requirements
- A variety of selectable coding challenges with detailed descriptions and examples.
- An embedded code editor for writing and editing code solutions.
- Immediate feedback after code submission, including correctness, print statements, and execution time.

## Non-functional Requirements
- **Performance**: Rapid code execution and feedback with minimal latency.
- **Security**: Safe execution of user-submitted code in an isolated environment.
- **Usability**: Clear, intuitive user interface with straightforward instructions.
- **Scalability**: Capability to handle high traffic and multiple simultaneous requests.
- **Extensibility**: Facility to add and update challenges without hassle.

## Constraints
- **Security**: Isolation of user code to prevent system damage.
- **Resource Usage**: Measures to limit resource consumption per submission.
- **Browser Compatibility**: Consistent performance across all major web browsers.
- **Execution Timeout**: Time limitations on code execution to prevent system slowdown.


## Getting Started

### Prerequisites

To run this project, you'll need to have the following installed:
- Python (3.10 or above)
- MySQL (8 or above)
- Docker (sandbox environment)

### Python Dependencies

The project relies on several Python packages:
1. `flask` - for the web server framework [built with 3.0.0].
2. `mysql-connector-python` - for interacting with MySQL databases [built with 8.1.0].
3. `python-dotenv` - for managing environment variables [built with 1.0.0].
4. `docker` - for container management [built with 6.1.3].

### Installation

1. Clone the repo
   `git clone https://github.com/your_username_/Project-Name.git`
2. Install required packages
   `pip install flask mysql-connector-python python-dotenv docker`
3. Local Development Prerequisites
   - Ensure you have MySQL installed on your local machine for database management.
   - Run the provided build.sql script
   - **Docker is required for running the code submissions inside a sandboxed environment. The application is designed to only work with docker, not with your native system.**
## Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request