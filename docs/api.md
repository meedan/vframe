# API Documentation

## POST /api/v1/match

Check if an image is in the database.  If no images are found matching the image, this image will be added to the database.

### Form parameters

- `limit` (default: 1) - Number of results to return.
- `url` - Image URL to fetch and test.  Will be added if not found.

While it is possible to query this API with a file, we only index URLs - this service does not provide image hosting.

### Response

Returns a JSON object with the following properties:

- `success` - True or false based on whether the query is successful.
- `error` - If success is false, the error code will be here.
- `match` - True if a match was found.
- `added` - True if no match was found, and the image was added to the database.
- `results` - Array containing the image that matched, if any.
- `timing` - Time in seconds to query the database.

## POST /api/v1/similar

Find similar images to a query image.

### Form parameters

- `threshold` (default: 20) - Minimum similarity threshold.
- `limit` (default: 10) - Number of results to return.
- `offset` (default: 0) - Query offset
- `url` - Image URL to fetch and test
- `q` (file) - Uploaded file to test

### Response

- `success` - True or false based on whether the query is successful.
- `error` - If success is false, the error code will be here.
- `match` - True if a match was found.
- `results` - Array containing the images that matched.
- `timing` - Time in seconds to query the database.

### Results

All search results contain the following fields:

- `id` - ID of the row in MySQL.
- `sha256` - SHA256 hash of the original file.
- `phash` - Perceptual hash of the file.
- `ext` - Image type.
- `url` - URL to the image.
- `score` - Perceptual hash distance from the query image. `0` is the best match possible, `64` is the worst.
