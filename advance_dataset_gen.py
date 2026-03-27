import json
import random

def generate_lecture_dataset():
    """
    Generates a structured synthetic dataset of noisy lectures and their academic notes.
    """
    topics = [
        {
            "topic": "Binary Search",
            "noisy": "uh today we talk about binary search it is faster than linear search um it divides array into two parts every time and you know it's logarithmic complexity so like O(log n). um you need a sorted array first for it to work.",
            "notes": "📘 Title: Binary Search Mechanics\n📌 Key Points:\n1. Efficiency: Binary search is significantly faster than linear search, offering O(log n) time complexity.\n2. Divide and Conquer: The algorithm works by repeatedly dividing the search space in half.\n3. Requirement: Binary search requires a pre-sorted array to function correctly."
        },
        {
            "topic": "Quantum Entanglement",
            "noisy": "so okay um quantum entanglement is like when two particles are interconnected uh even when separated by light-years distance they stay together like um Einstein called it spooky action at a distance. measuring one instant affects the other. you know its a core part of quantum computing.",
            "notes": "📘 Title: Quantum Entanglement and Non-locality\n📌 Key Points:\n1. Particle Interconnection: Particles become linked so that the state of one is instantly connected to the other regardless of distance.\n2. Spooky Action: Historically referred to as 'spooky action at a distance' due to its counter-intuitive nature.\n3. Technological Role: It serves as a fundamental principle behind the development of quantum computing and communication."
        },
        {
            "topic": "Photosynthesis",
            "noisy": "uh well chloroplasts um they capture light energy and start photosynthesis uh basically plants turn water and CO2 into glucose like sugar and they release oxygen. it happens in two stages light-dependent and light-independent um Calvin cycle is the second one.",
            "notes": "📘 Title: Phases of Photosynthesis\n📌 Key Points:\n1. Energy Conversion: Plants convert light energy, water, and CO2 into chemical energy (glucose).\n2. Oxygen Production: Oxygen is released as a vital byproduct of the process.\n3. Dual-Stage Process: It consists of light-dependent reactions followed by the light-independent Calvin cycle."
        },
        {
            "topic": "French Revolution",
            "noisy": "so the french revolution um started in 1789 because of like many things like famine and financial crisis and well the rise of the third estate wanting rights uh it ended with napoleon taking power. the reign of terror was like a very um dark part of it with robespierre.",
            "notes": "📘 Title: The French Revolution: Causes and Outcomes\n📌 Key Points:\n1. Socio-Economic Origins: Triggered by 1789 famine, national debt, and class inequality.\n2. Radical Shifts: Featured the 'Reign of Terror' led by Maximilien Robespierre.\n3. Political Transition: Culminated in the fall of the monarchy and the eventual rise of Napoleon Bonaparte."
        },
        {
            "topic": "Python Lists",
            "noisy": "okay so like python lists are ordered and changeable. you can have different types inside like integers and strings um you use append to add to the end of the list. uh they are indexed starting from zero which is important to remember.",
            "notes": "📘 Title: Characteristics of Python Lists\n📌 Key Points:\n1. Dynamic Properties: Lists are ordered, mutable, and can store heterogeneous data types.\n2. Modification: Elements can be added systematically using the .append() method.\n3. Indexing: Zero-based indexing system is used for accessing elements."
        },
        {
            "topic": "Thermodynamics",
            "noisy": "um the first law of thermodynamics is basically energy cannot be created or destroyed uh only transformed from one form to another so like heat into work. the second law says entropy um usually increases which means more disorder over time.",
            "notes": "📘 Title: Fundamental Laws of Thermodynamics\n📌 Key Points:\n1. Conservation of Energy: First law states energy is transformed, never created or destroyed.\n2. Entropy: Second law establishes that the total entropy of an isolated system always increases.\n3. Energy Flow: Focuses on how heat energy is converted into mechanical work."
        },
        {
            "topic": "Economics - Supply and Demand",
            "noisy": "uh so demand is how much people want something. supply is how much exists. um when demand goes up and supply stays same price usually goes up too. it's like a balance in the market equilibrium you know.",
            "notes": "📘 Title: Principles of Market Equilibrium\n📌 Key Points:\n1. Market Factors: Prices are determined by the interaction between supply (availability) and demand (consumer desire).\n2. Inverse Relationships: Shifts in demand or supply lead to price fluctuations.\n3. Equilibrium: The point where supply equals demand is known as the market equilibrium."
        },
        {
            "topic": "Machine Learning - Supervised Learning",
            "noisy": "okay um supervised learning is where you use labeled data to train a model. you have inputs and expected outputs like uh spam detection where you know which emails are spam. regressson and classification are the two main types um of supervised learning.",
            "notes": "📘 Title: Introduction to Supervised Learning\n📌 Key Points:\n1. Labeled Training: Models are trained using datasets that include both inputs and the correct outputs (labels).\n2. Pattern Recognition: The system learns to map new inputs to correct labels based on historical data.\n3. Categorization: Divided primarily into regression (predicting continuous values) and classification (sorting data)."
        },
        {
            "topic": "Blockchain Technology",
            "noisy": "uh decentralization is key. blockchain is like a distributed ledger um where every block is linked with a hash. transparency and security uh make it great for finance like bitcoin. um consensus algorithms like proof of work keep it honest.",
            "notes": "📘 Title: Blockchain and Decentralized Ledgers\n📌 Key Points:\n1. Distributed Architecture: Functions as a decentralized, immutable ledger shared across a network.\n2. Cryptographic Security: Blocks are secured using unique hashes, ensuring data integrity.\n3. Network Trust: Relies on consensus mechanisms like Proof of Work to validate transactions without a central authority."
        },
        {
            "topic": "Psychology - Classical Conditioning",
            "noisy": "so Pavlov um noticed that dogs began to salivate when they saw the person who fed them. this is classical conditioning uh where a neutral stimulus gets associated with an unconditional one. the bell becomes a conditioned stimulus um after many repetitions.",
            "notes": "📘 Title: Foundations of Classical Conditioning\n📌 Key Points:\n1. Associative Learning: A process where a neutral stimulus evokes a response after being paired with a natural stimulus.\n2. Pavlovian Theory: Originated from Ivan Pavlov's research on canine digestive responses.\n3. Conditioned Response: Over time, the subject learns to react to the previously neutral stimulus in anticipation of the reward."
        },
        {
            "topic": "Chemistry - Atomic Structure",
            "noisy": "atoms have a nucleus with protons and neutrons um then you have electrons in shells around it. the atomic number is the number of protons. uh isotopes have the same protons but different numbers of neutrons um changing their weight.",
            "notes": "📘 Title: Elements of Atomic Theory\n📌 Key Points:\n1. Core Components: Atoms consist of a central nucleus containing protons and neutrons, orbited by electrons.\n2. Identity: The number of protons determines the chemical identity (Atomic Number).\n3. Isotopic Variance: Different versions of an element exist with varying neutron counts, affecting mass but not chemical behavior."
        },
        {
            "topic": "Geography - Plate Tectonics",
            "noisy": "the earth's crust is made of plate um which move on the mantle. continental drift was proposed by Wegener uh and now we call it plate tectonics. where they meet you get earthquakes or volcanoes um specially in the ring of fire.",
            "notes": "📘 Title: Dynamics of Plate Tectonics\n📌 Key Points:\n1. Tectonic Activity: The lithosphere is divided into plates that move and interact on the viscous mantle layer.\n2. Geological Transitions: Interactions at plate boundaries are the primary cause of seismic and volcanic activity.\n3. Historical Context: Evolved from Alfred Wegener's theory of continental drift into a comprehensive scientific model."
        },
        {
            "topic": "Roman Empire Expansion",
            "noisy": "so Rome um started as a small city-state but then it conquered like most of Europe and North Africa. they had a very efficient military system um with legions. their roads and laws uh created stability in what we call Pax Romana after Augustus took over.",
            "notes": "📘 Title: The Rise and Maturity of the Roman Empire\n📌 Key Points:\n1. Military Hegemony: Expansion was driven by superior organization and the disciplined Roman legion system.\n2. Infrastructural Stability: Extensive road networks and legal systems unified diverse territories.\n3. Imperial Peace: The 'Pax Romana' marked a period of relative calm and cultural growth under early emperors."
        },
        {
            "topic": "Quantum Computing Qubits",
            "noisy": "traditional bits are 0 or 1. but qubits um using superposition can be both at the same time. it allows massive parallel processing uh for certain algorithms like Shor's algorithm for breaking encryption um and it's very sensitive to noise.",
            "notes": "📘 Title: Principles of Quantum Information\n📌 Key Points:\n1. Bit Revolution: Unlike binary bits, qubits utilize superposition to exist in multiple states simultaneously.\n2. Computational Scaling: Enables exponential processing power for specific complex algorithms.\n3. Sensitivity: Systems are highly susceptible to environmental decoherence and quantum noise."
        },
        {
            "topic": "Artificial Intelligence Ethics",
            "noisy": "bias in data is a big problem. if the training data is biased the AI will be biased too uh like in facial recognition. transparency and explainability are needed um to ensure safety. we need regulations to protect privacy.",
            "notes": "📘 Title: Ethical Frameworks in AI Development\n📌 Key Points:\n1. Algorithmic Bias: Systems risk inheriting and amplifying prejudices present in their training datasets.\n2. Accountability: There is a critical need for transparent and explainable decision-making processes.\n3. Governance: Implementing regulatory guardrails is essential for protecting individual privacy and safety."
        }
    ]

    # Duplicate and augment slightly to create a larger base for training
    dataset = []
    instruction = "Transform lecture into structured academic notes."
    
    for item in topics:
        dataset.append({
            "instruction": instruction,
            "topic": item["topic"],
            "input": item["noisy"],
            "structured_notes": item["notes"]
        })
    
    # Save to file
    with open("dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"Generated {len(dataset)} examples in dataset.json")

if __name__ == "__main__":
    generate_lecture_dataset()
