import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatInputModule } from '@angular/material';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CseeLoginComponent } from './csee-login/csee-login.component';
import { CseeHwComponent } from './csee-hw/csee-hw.component';
import { Routes, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HwRegisterComponent } from './csee-hw/hw-register/hw-register.component';
import { HwManageComponent } from './csee-hw/hw-manage/hw-manage.component';
import { CseeSignupComponent } from './csee-signup/csee-signup.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { HwDetailComponent } from './csee-hw/hw-detail/hw-detail.component';
import { CseeAuthComponent } from './csee-auth/csee-auth.component';

import { FilterPipe } from './filter.pipe';   
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime';

export const ROUTES:Routes = [
    { path: 'signup/csee', component: CseeSignupComponent },
    { 
      path: 'professor-page', 
      component: CseeHwComponent,
      children : [
          { path: '', component: HwRegisterComponent},    
          { path: 'scoreboard/:id', component: HwManageComponent },
          { path: 'scoreboard/:id/:std_id', component: HwDetailComponent },
      ]
    },
    {
      path: 'professor-auth',
      component : CseeAuthComponent,
    }
]

@NgModule({
  declarations: [FilterPipe, CseeLoginComponent, CseeHwComponent, HwRegisterComponent, HwManageComponent, CseeSignupComponent, HwDetailComponent, CseeAuthComponent],
  imports: [
    CommonModule,
    RouterModule.forRoot(ROUTES),
    FormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    BrowserAnimationsModule,
    FontAwesomeModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
  ]
})
export class CseeModule { }
