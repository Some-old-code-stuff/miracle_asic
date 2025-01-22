/**
 * Created by mrakolice on 11.09.18.
 */

import axios from 'axios'
import {SERVER_URL, NEW_SERVER_URL} from './serverUrl'

export const HTTP = axios.create({
  baseURL: SERVER_URL + '/profile'
});

export const newHTTP = axios.create({
  baseURL: NEW_SERVER_URL +  '/apiv2'
});

export const PAGE_COUNT = 100;
