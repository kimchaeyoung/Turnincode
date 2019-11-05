import { Component, OnInit } from '@angular/core';
import { UserService } from '../../../user.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-hw-register',
  templateUrl: './hw-register.component.html',
  styleUrls: ['./hw-register.component.css'],
  providers: [UserService]
})
export class HwRegisterComponent implements OnInit {
  register;
  hwlist : any = [];  

  constructor(private http:HttpClient, route: ActivatedRoute, private userService: UserService, private router:Router) { 
    this.http.get('./professor-page/getregister/').subscribe(
	response=> {
            this.hwlist = response;
	},
	error => console.log('error',error)
      ) 
  }

  ngOnInit() {
      this.register = {
          hw_name: '',
      	  hw_description: '',
      	  hw_duedate: '',
       }   
  }

  Register(hw_id){
    this.userService.registerHomework(this.register, hw_id).subscribe(
      response => {
        this.router.navigateByUrl('professor-page');
      },
      error => console.log('error', error)
    )
  }
}

