import { Component, OnInit } from '@angular/core';
import { FilesService } from './shared/services/files.service';
import { finalize } from 'rxjs';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'study_bench';
  filesList : string[] = [];

 formData : any = undefined;

  loadings = {
    listing : false
  }

  constructor(private files: FilesService){}

  ngOnInit(){
    this.getFilelist()
  }

  public getFilelist(){
    this.loadings.listing = true;
    this.files.getFiles().pipe(finalize(()=>{
      this.loadings.listing = false;
    })).subscribe({
      next : (res) => {
        this.filesList = res.files
      },
      error : (err)=>{
        console.error(err)
      }
    })
  }

  public uploadFile(){
    if(this.formData)
    this.files.uploadFile(this.formData).subscribe({
      next : ()=>{
        this.getFilelist()
      }
    })
  }

  public saveFile(event : any){
    const file = event.target.files[0];
    this.formData = new FormData();
    this.formData.append('file', file);
  }

  public getSummary(file_name : string){
    this.files.getFileSummary(file_name).subscribe({
      next : (res)=>{
        console.log(res)
      }
    })
  }
}
