
// Step 2: Switch to bookstore database
db = db.getSiblingDB("bookstore");

// Step 3: Load authors.json
db.authors.drop();
let authors = JSON.parse(fs.readFileSync("authors.json", "utf8"));
db.authors.insertMany(authors);

// Step 4: Load books.json
db.books.drop();
let books = JSON.parse(fs.readFileSync("books.json", "utf8"));
db.books.insertMany(books);

// Step 5: List all authors and books
db.authors.find();
db.books.find();

// Step 6: Insert two new books
db.books.updateOne(
  { title: "Harry Potter and the Sorcerer's Stone" },
  {
    $set: {
      title: "Harry Potter and the Sorcerer's Stone",
      published_year: 1997,
      author_ids: ["author_004"]
    }
  },
  { upsert: true }
);

db.books.updateOne(
  { title: "Percy Jackson and the Lightning Thief" },
  {
    $set: {
      title: "Percy Jackson and the Lightning Thief",
      published_year: 2005,
      author_ids: ["author_005"]
    }
  },
  { upsert: true }
);

// Step 7: Add missing authors
db.authors.updateOne(
  { _id: "author_004" },
  {
    $set: {
      name: "J.K. Rowling",
      nationality: "British",
      bio: {
        short: "British author best known for the Harry Potter series.",
        long: "J.K. Rowling is a British author best known for writing the Harry Potter fantasy series, which follows a young wizard attending Hogwarts School of Witchcraft and Wizardry."
      }
    }
  },
  { upsert: true }
);

db.authors.updateOne(
  { _id: "author_005" },
  {
    $set: {
      name: "Rick Riordan",
      nationality: "American",
      bio: {
        short: "American author best known for the Percy Jackson series.",
        long: "Rick Riordan is an American author known for writing the Percy Jackson and the Olympians series, which combines Greek mythology with modern adventures."
      }
    }
  },
  { upsert: true }
);

// Step 8: Filter books by a list of authors
db.books.find({
  author_ids: {
    $in: ["author_001", "author_004"]
  }
});


