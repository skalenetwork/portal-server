# SKALE Portal Server

[![Discord](https://img.shields.io/discord/534485763354787851.svg)](https://discord.gg/vvUtWJB)

SKALE Portal Server is a Flask-based backend application that provides authentication and app management functionality for the SKALE Portal.

## Prerequisites

- Python 3.9+
- MySQL 5.7+
- Docker (optional, for containerized deployment)

## Configuration

```bash
MYSQL_USER=user
MYSQL_ROOT_PASSWORD=root_password
MYSQL_PASSWORD=password
SECRET_KEY=secret_key
DOMAIN_NAME=portal-server.com
```

SLL certs:

Put `fullchain.pem` and `privkey.pem` in the `ssl_certs` directory.

To use with SSL certs, update the `ssl.conf` file in the `nginx` directory with your SSL certificate paths.

## API Endpoints

- `/api/auth/nonce` (GET): Get a nonce for authentication
- `/api/auth/signin` (POST): Sign in with Ethereum
- `/api/auth/signout` (POST): Sign out
- `/api/auth/status` (GET): Check authentication status
- `/api/apps/like` (POST): Like an app
- `/api/apps/unlike` (POST): Unlike an app
- `/api/apps/liked` (GET): Get user's liked apps
- `/api/apps/all` (GET): Get all apps and their like counts

## Deployment

```
docker compose up --build
```

## Development

#### Pre-commit hook

```bash
ruff check app/
```

#### Format code

```bash
ruff format app/
```

## License

![GitHub](https://img.shields.io/github/license/skalenetwork/skale.py.svg)

All contributions are made under the [GNU Affero General Public License v3](https://www.gnu.org/licenses/agpl-3.0.en.html). See [LICENSE](LICENSE).
