# Check Image Deduplication API

- Draft April 13, 2019  
- Specs from "VFRAME - SHARED Image Matching - Checkpoint Spec 2019APR.odt"


The VFRAME/Check image deduplication API will provide capabilities to determine if a query image matches any of prior submitted query images. 

Functional Requirements:

- provide matching results for at least 10,000 image requests submitted per day
- provide scalable capacity for sustained usage of at least one year
- provide an authenticated API service to match a query image to all previously submitted query images and receive a match result


## Use Case Scenario

User story:
- Audience member sends image to a number on WhatsApp (or generically, user adds an image to Check). - Handled by Smooch.
    • Image is ingested into Check. - Handled by Smooch & Check.
    • Image is matched against existing images in Check.
        ◦ MVP:
            ▪ detect near-identical matches that are different sizes, resolutions.
        ◦ Assess for feasibility:
            ▪ find same meme images used for different claims
            ▪ find same claims using different meme images
            ▪ find same images (not memes) with different text
            ▪ find same images + text in different physical files
    • Image is automatically related to any matching images in Check.
    • Analyst can confirm matches and dissociate any false matches. - Handled in Check
    • Audience member receives the verification result for any matching images with existing final-status. - Handled in Check, Smooch, and WA Business API
    
    
## Out of Scope

- Video matching
- Machine vision or content analysis
- Indian-language OCR (though OCR models/ libraries should be easily integrated)
- User-in-the-loop machine learning for improvement of matching algorithms
    
    

## Example Requests

All requests are standard multipart POST requests.  Specify the image with the parameter `image`.

Example response for a successful image upload with no match:

`check.vframe.io/v1/api/match/`

```
{
  "success": True,
  "match": False
}
```
 			 

Example response for a successful image upload with a match, within the standard similarity threshold:

`check.vframe.io/v1/api/match/`

```
{
  "success": True,
  "match": True,
  "closest_match": {
  	"sha256: "ed294c4a0bf1fc7120fe3fde8d96a9ac",
  	"score": 0
  }
}
"
```

Get match, but with more permissive threshold

`check.vframe.io/v1/api/match/?threshold=10`

```
{
  "success": True,
  "match": True,
  "closest_match": {
    "sha256: "efbaaffdcc01e45461b41dd2294020c4",
    "score": 7
  },
}
```

Get top similar matches, but with more permissive threshold

`check.vframe.io/v1/api/similar/`

