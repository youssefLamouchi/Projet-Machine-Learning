import { Routes } from '@angular/router';
import { TrainComponent } from './components/train/train.component';
import { PredictComponent } from './components/predict/predict.component';

export const routes: Routes = [
  { path: '', redirectTo: '/train', pathMatch: 'full' },
  { path: 'train', component: TrainComponent },
  { path: 'predict', component: PredictComponent }
];
