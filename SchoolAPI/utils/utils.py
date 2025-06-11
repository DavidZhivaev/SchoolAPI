import jwt # type: ignore
from errors.errors import LibError
from urllib.parse import urlparse, parse_qs, unquote
import json


class Utils:
    def getNormalDate(year, month, day):
        return f"{year}-{month:02}-{day:02}"
    
    def getJwtInfo(text: str):
        try:
            return jwt.decode(text, options={"verify_signature": False})
        except jwt.exceptions.DecodeError as e:
            raise LibError("Error decoding!")
        
    def extractUuid(url: str):
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            if 'context' not in query_params:
                return None
                
            context_token = query_params['context'][0]
            
            try:
                return Utils.getJwtInfo(context_token)['mi']
            except jwt.exceptions.DecodeError:
                try:
                    return json.loads(unquote(context_token))['mi']
                except json.JSONDecodeError:
                    return None
                    
        except Exception as e:
            raise LibError("Error parsing!")