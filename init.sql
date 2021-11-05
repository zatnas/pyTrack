CREATE TABLE 'Account' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL,
color TEXT NOT NULL
);

CREATE TABLE 'CategoryGroup' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL,
color TEXT NOT NULL,
icon TEXT NOT NULL
);

CREATE TABLE 'Category' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
categorygroup_id INTEGER NOT NULL,
name TEXT NOT NULL,
color TEXT NOT NULL,
icon TEXT NOT NULL,
FOREIGN KEY (categorygroup_id) REFERENCES 'CategoryGroup'(id)
);

CREATE TABLE 'Attachment' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
path TEXT NOT NULL
);

CREATE TABLE 'TransactionGroup' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
attachment_id INTEGER,
datetime INTEGER NOT NULL,
note TEXT,
place TEXT,
FOREIGN KEY (attachment_id) REFERENCES 'Attachment'(id)
);

CREATE TABLE 'Transaction' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
account_id INTEGER NOT NULL,
category_id INTEGER NOT NULL,
transactiongroup_id INTEGER,
attachment_id INTEGER,
datetime INTEGER NOT NULL,
amount REAL NOT NULL,
note TEXT,
place TEXT,
FOREIGN KEY (account_id) REFERENCES 'Account'(id),
FOREIGN KEY (category_id) REFERENCES 'Category'(id),
FOREIGN KEY (transactiongroup_id) REFERENCES 'TransactionGroup'(id),
FOREIGN KEY (attachment_id) REFERENCES 'Attachment'(id)
);

CREATE TABLE 'Tag' (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL,
color TEXT NOT NULL
);

CREATE TABLE 'TransactionTag' (
transaction_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL,
FOREIGN KEY (transaction_id) REFERENCES 'Transaction'(id),
FOREIGN KEY (tag_id) REFERENCES 'Tag'(id),
PRIMARY KEY (transaction_id, tag_id)
);

CREATE TABLE 'TransactionGroupTag' (
transactiongroup_id INTEGER NOT NULL,
tag_id INTEGER NOT NULL,
FOREIGN KEY (transactiongroup_id) REFERENCES 'TransactionGroup'(id),
FOREIGN KEY (tag_id) REFERENCES 'Tag'(id),
PRIMARY KEY (transactiongroup_id, tag_id)
);
