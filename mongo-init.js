db.createUser(
  {
      user: "doaa",
      pwd: "doaapass",
      roles: [
          {
              role: "readWrite",
              db: "qca_logging_db"
          }
      ]
  }
);
