import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
/**
 * Componente de dashboard para métricas.
 */
export class DashboardComponent {
  /**
   * Carrega métricas iniciais da API.
   */
  ngOnInit(): void {
    this.loadMetrics();
  }

  /**
   * Atualiza o gráfico com filtros aplicados.
   */
  refresh(filters: string[]): string {
    return `Atualizado com ${filters.length} filtros`;
  }

  private loadMetrics(): void {
    // TODO: chamar endpoint real
  }
}
