FROM python@sha256:8f642902ba368481c9aca0a100f08daf93793c6fa14d3002253ea3cd210383a7 as base

WORKDIR /opt

ARG USER_UID=1000
RUN adduser --shell /bin/sh --system --group --uid "${USER_UID}" default

RUN chown -R default /opt

USER default

ENV VIRTUAL_ENV="/home/default/.cache/pypoetry/virtualenvs"
ENV PATH "$VIRTUAL_ENV/bin:/home/default/.local/bin:$PATH"

FROM base as builder

RUN pip install poetry
COPY --chown=default:default poetry.lock pyproject.toml ./
RUN mkdir -p ./src/project_template/__init__.py

ARG NO_DEV="-v"

RUN poetry install --remove-untracked "$NO_DEV"

FROM base as final

COPY --chown=default:default . .
COPY --chown=default:default --from=builder "$VIRTUAL_ENV" "$VIRTUAL_ENV"

ARG DEBUG="true"
ENV DEBUG=$DEBUG

ARG ENVIRONMENT="local"
ENV ENVIRONMENT=$ENVIRONMENT

ENV SQLALCHEMY_WARN_20=1

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
CMD ["python", "src/project_template/main.py"]
