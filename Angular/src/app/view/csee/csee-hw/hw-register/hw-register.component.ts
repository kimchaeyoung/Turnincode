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
  hw_id = '';
  hw_base = '';
  hw_eval = '';
  hw_madeby = '';

  constructor(private http:HttpClient, route: ActivatedRoute, private userService: UserService, private router:Router) { 
    this.hw_id = route.snapshot.params['id']; 
    this.http.get('./professor-page/getregister/'+this.hw_id).subscribe(
	response=> {
                this.hw_base = response[0];
                this.hw_eval = response[1];
                this.hw_madeby = response[2];
              
              
	},
	error => console.log('error',error)
      ) 
  }

  ngOnInit() {
      this.register = {
          hw_name: '',
      	  hw_base: '',
      	  hw_eval: '',
      	  hw_description: '',
      	  hw_duedate: '',
          hw_madeby: '',
     };   
  }

  Register(){
    this.register.hw_base = this.hw_base;
    this.register.hw_eval = this.hw_eval;
    this.register.hw_madeby = this.hw_madeby;

    this.userService.registerHomework(this.register, this.hw_id).subscribe(
      response => {
        this.router.navigateByUrl('professor-page');
      },
      error => console.log('error', error)
    )
  }
}
