import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http'

const URL = 'http://127.0.0.1:5000'

@Injectable({
  providedIn: 'root'
})
export class FilesService {

  constructor(private _http: HttpClient){ }

  public getFiles(){
    return this._http.get<{files : string[]}>(URL + '/files')
  }

  public uploadFile(file : any){
    return this._http.post(URL + '/upload',file)
  }

  public getFileSummary(file_name : string){
    return this._http.post(URL + '/summary',{
      params : {
        file_name : file_name
      }
      
    })
  }
}
