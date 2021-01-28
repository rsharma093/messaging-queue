CREATE TABLE process (
  id integer primary key autoincrement,
  func_name string not null,
  status string not null,
  priority string not null,
  output string,
  func_params string,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);