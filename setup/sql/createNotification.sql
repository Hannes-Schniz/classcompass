CREATE TABLE notifications(
    notificationID INTEGER PRIMARY KEY,
    message,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    hash,
    plattform,
    destination
)