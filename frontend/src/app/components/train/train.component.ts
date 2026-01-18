import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MlService } from '../../services/ml.service';

@Component({
  selector: 'app-train',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './train.component.html',
  styleUrl: './train.component.css'
})
export class TrainComponent {
  selectedFile: File | null = null;
  loading = false;
  result: any = null;
  error: string | null = null;

  constructor(private mlService: MlService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.result = null;
    this.error = null;
  }

  trainModel() {
    if (!this.selectedFile) {
      this.error = 'Veuillez sélectionner un fichier CSV';
      return;
    }

    this.loading = true;
    this.error = null;

    this.mlService.trainModel(this.selectedFile).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.error || 'Erreur lors de l\'entraînement';
        this.loading = false;
      }
    });
  }
}
