import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MlService } from '../../services/ml.service';

@Component({
  selector: 'app-predict',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './predict.component.html',
  styleUrl: './predict.component.css'
})
export class PredictComponent {
  selectedFile: File | null = null;
  loading = false;
  predictions: number[] = [];
  error: string | null = null;

  constructor(private mlService: MlService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.predictions = [];
    this.error = null;
  }

  makePredictions() {
    if (!this.selectedFile) {
      this.error = 'Veuillez sélectionner un fichier CSV';
      return;
    }

    this.loading = true;
    this.error = null;

    this.mlService.predict(this.selectedFile).subscribe({
      next: (response) => {
        this.predictions = response.predictions;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.error || 'Erreur lors de la prédiction';
        this.loading = false;
      }
    });
  }

  getAverage(): string {
    if (this.predictions.length === 0) return '0.00';
    const sum = this.predictions.reduce((a, b) => a + b, 0);
    return (sum / this.predictions.length).toFixed(2);
  }

  getMin(): string {
    if (this.predictions.length === 0) return '0.00';
    return Math.min(...this.predictions).toFixed(2);
  }

  getMax(): string {
    if (this.predictions.length === 0) return '0.00';
    return Math.max(...this.predictions).toFixed(2);
  }

  downloadPredictions() {
    const csv = 'Index,Usage_kWh_Predicted\n' + 
      this.predictions.map((p, i) => `${i},${p}`).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'predictions.csv';
    a.click();
  }
}
