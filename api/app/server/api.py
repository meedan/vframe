import io
import os
import re
import time
import logging
import json
from pathlib import Path
import urllib.request

import numpy as np
from flask import Blueprint, request, jsonify
from PIL import Image

from app.models.sql_factory import search_by_phash, add_phash
from app.utils.im_utils import compute_phash_int
from app.utils.file_utils import sha256_stream

sanitize_re = re.compile('[\W]+')
valid_exts = ['.gif', '.jpg', '.jpeg', '.png']

MATCH_THRESHOLD = 1
MATCH_LIMIT = 1

SIMILAR_THRESHOLD = 20
SIMILAR_LIMIT = 10

api = Blueprint('api', __name__)

@api.route('/')
def index():
  """
  API status test endpoint
  """
  return jsonify({ 'status': 'ok' })

def fetch_url(url):
  """
  Fetch an image from a URL and load it
  """
  if not url:
    return None, 'no_image'
  basename, ext = os.path.splitext(url)
  if ext.lower() not in valid_exts:
    return None, 'not_an_image'
  ext = ext[1:].lower()

  remote_request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  remote_response = urllib.request.urlopen(remote_request)
  raw = remote_response.read()
  im = Image.open(io.BytesIO(raw)).convert('RGB')
  return raw, im

def get_params(default_threshold=MATCH_THRESHOLD, default_limit=MATCH_LIMIT):
  """
  Normalize parameters from request.form
  """
  try:
    threshold = int(request.form.get('threshold') or default_threshold)
    limit = int(request.form.get('limit') or default_limit)
    offset = int(request.form.get('offset') or 0)
    context = json.loads(request.form.get('context') or '{}')
    filter =  json.loads(request.form.get('filter') or '{}')
  except:
    return None, 'param_error'

  # Process uploaded file
  if 'q' in request.files:
    file = request.files['q']
    fn = file.filename
    # demo client currently uploads a jpeg called 'blob'
    if fn.endswith('blob'):
      logging.debug('received a blob, assuming JPEG')
      fn = 'filename.jpg'

    basename, ext = os.path.splitext(fn)
    if ext.lower() not in valid_exts:
      return None, 'not_an_image'
    ext = ext[1:].lower()

    raw = None
    im = Image.open(file.stream).convert('RGB')
    url = None

  # Fetch remote URL
  else:
    url = request.form.get('url')
    ext = Path(url).suffix.replace('.','')
    raw, im = fetch_url(url)
    if raw is None:
      return raw, im # error
  return (threshold, limit, offset, url, ext, raw, im, context, filter,), None


@api.route('/v1/match', methods=['POST'])
def match():
  """
  Search by uploading an image
  """
  params, error = get_params(default_threshold=MATCH_THRESHOLD, default_limit=MATCH_LIMIT)
  if error:
    return jsonify({
      'success': False,
      'match': False,
      'added': False,
      'error': error,
    })

  threshold, limit, offset, url, ext, raw, im, context, filter = params

  start = time.time()

  phash = compute_phash_int(im)

  results = search_by_phash(phash=phash, threshold=threshold, limit=limit, offset=0, filter=filter)
  match = False
  added = False

  if len(results) == 0:
    if url:
      hash = sha256_stream(io.BytesIO(raw))
      added = add_phash(sha256=hash, phash=phash, ext=ext, url=url, context=context)
  else:
    match = True

  logging.debug('query took {0:.2g} s.'.format(time.time() - start))

  return jsonify({
    'success': True,
    'match': match,
    'added': added,
    'results': results,
    'timing': time.time() - start,
  })


@api.route('/v1/similar', methods=['POST'])
def similar():
  """
  Search by uploading an image
  """
  params, error = get_params(default_threshold=SIMILAR_THRESHOLD, default_limit=SIMILAR_LIMIT)
  if error:
    return jsonify({
      'success': False,
      'match': False,
      'error': error,
    })

  threshold, limit, offset, url, ext, raw, im, context, filter = params

  start = time.time()

  phash = compute_phash_int(im)
  ext = ext[1:].lower()

  results = search_by_phash(phash=phash, threshold=threshold, limit=limit, offset=offset, filter=filter)

  if len(results) == 0:
    match = False
  else:
    match = True

  logging.debug('query took {0:.2g} s.'.format(time.time() - start))

  return jsonify({
    'success': True,
    'match': match,
    'results': results,
    'timing': time.time() - start,
  })
