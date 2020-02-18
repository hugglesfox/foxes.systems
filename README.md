# Blog

Idk why but I wrote my own static cms.

## Writing Posts

Posts go in `content/posts` and are formatted in Markdown.
The basic structure is as follows:

```Markdown
// The first line of the document(which must contain a header 1) is used as
// the blog title
# Title

// The first occurrence of a * is used for the date which must be formatted
// like so
*Month(March) day_num(1), Year(2018)*

// A header image can be inserted here if wanted

// The first paragraph is used for the description/summary
Insert some content here. This will be shown on the home page as a description.


Here is another paragraph containing more markdown formatted content.
```

## Generating a static site

**Note:** This assumes you already have all the python deps installed
(`pipenv install`) as well having the css, js and rust code compiled
(see Compiling stuffs).

```
$ python3 -m blog
```

The `public` directory should now contain a static version of the blog

## Running dev server

```
$ FLASK_DEBUG=True FLASK_APP=blog flask run 
```

## Compiling stuffs

This project is a mishmash of code.

### Webpack (`Scss`/`Js`)

```
$ npm run build
```

### Rust

**Note:** This project depends on rust nightly.

**Note:** Matruin is a python application thus is installed as a
dev dependency by pipenv.

```
$ maturin develop
```

## Random things to note

  - Code highlighting is supported; Provided by pygments
  - `blog/static/` is where to throw static stuffs like images
  - Js and SCSS is stored in `blog/src/`
  - `src/` is for rust source code
