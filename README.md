# MUNTree

MUNTree is an alterantive to linktree for private use.

To Do:

- [x] Make backend (mostly ai but tested)

- [x] Make frontend

- [x] Dockerize (integrate frontend + backend in docker)

- [ ] Allow to reposition the links

- [ ] Add rate limiting.

- [ ] Add stats for the visitors.

- [ ] Add logging.


## How to run the application?

Run the following command to copy the file from `backend/.env.sample` to `backend/.env` by `cp backend/.env.sample backend/.env` and now, modify it according to your requirements.

Run the following command to build the image and start the container.

`docker compose up -d`

The frontend will now be visible at:

`http://localhost:4321/`

This can be changed by modifying docker-compose.yml:23

---

Made with 💙 by MunSoc Tech Team 2025-26.
