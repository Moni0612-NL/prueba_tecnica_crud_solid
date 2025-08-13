from time import sleep

class BarridoService:
    def __init__(self, api_service, registro_repo, barrido_repo, per_call_delay=0.12):
        self.api_service = api_service
        self.registro_repo = registro_repo
        self.barrido_repo = barrido_repo
        self.per_call_delay = per_call_delay

    def run_full_barrido(self, max_sweeps=50):
        sweeps = 0
        while sweeps < max_sweeps:
            bads = self.registro_repo.get_bad()
            if not bads:
                break
            sweeps += 1
            improved = 0
            checked = len(bads)
            for r in bads:
                # hacemos una llamada extra
                try:
                    data = self.api_service.fetch_with_rate_limit()
                except Exception as e:
                    # si falla una llamada, solo contamos el intento, no rompemos todo
                    r.attempts += 1
                    self.registro_repo.update(r)
                    continue

                # cada llamada cuenta en attempts
                r.attempts += 1

                # actualizamos solo si mejora (medium o good)
                if data['category'] in ('medium', 'good'):
                    r.value = data['value']
                    r.category = data['category']
                    improved += 1

                self.registro_repo.update(r)
                sleep(self.per_call_delay)

            # logueamos el barrido
            self.barrido_repo.log_sweep(sweep_number=sweeps, records_checked=checked, records_improved=improved)

        return {"sweeps": sweeps}
