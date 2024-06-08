FROM coady/pylucene

RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

WORKDIR /app
COPY . .

ENTRYPOINT [ "./server.sh" ]
