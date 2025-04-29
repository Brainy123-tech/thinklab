def run_simulation(animal_type, simulation_speed):
    summary = f"The {animal_type} was tested under {simulation_speed} conditions."
    success_rate = {
        'slow': 95,
        'medium': 80,
        'fast': 60
    }.get(simulation_speed, 70)
    
    recommendations = [
        "Ensure food availability",
        "Monitor predator-prey balance",
        "Check environmental stressors"
    ]

    return {
        'summary': summary,
        'success_rate': success_rate,
        'recommendations': recommendations
    }
