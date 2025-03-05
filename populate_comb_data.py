# populate_comb_data.py

from db_setup import setup_database, COMBCategory, Indicator, CodingExample

def populate_comb_categories(session):
    """
    Add the 6 COM-B categories to the database as separate, equal categories.
    """
    categories = [
        {
            'name': 'Capability - Physical',
            'description': 'Physical skills, strength, or stamina needed to perform a behavior.'
        },
        {
            'name': 'Capability - Psychological',
            'description': 'Knowledge, psychological skills, mental strength or stamina to engage in necessary mental processes.'
        },
        {
            'name': 'Opportunity - Physical',
            'description': 'Opportunities afforded by the environment including time, resources, locations, cues, physical affordance.'
        },
        {
            'name': 'Opportunity - Social',
            'description': 'Opportunities afforded by interpersonal influences, social cues and cultural norms that influence the way we think about things.'
        },
        {
            'name': 'Motivation - Automatic',
            'description': 'Automatic processes involving emotional reactions, desires, impulses, inhibitions, drive states and reflex responses.'
        },
        {
            'name': 'Motivation - Reflective',
            'description': 'Reflective processes involving plans, evaluations, beliefs about what is good or bad, and conscious intentions.'
        }
    ]
    
    # Add all categories to the database
    for category_data in categories:
        category = COMBCategory(**category_data)
        session.add(category)
    
    # Commit the changes
    session.commit()
    
    # Return the created categories as a dictionary for easy reference
    return {cat.name: cat for cat in session.query(COMBCategory).all()}

def populate_indicators(session, categories):
    """
    Add positive and negative indicators for each category.
    """
    indicators_data = {
        'Capability - Physical': {
            'positive': [
                'Physical skill or ability to perform task',
                'Physical strength or stamina',
                'Dexterity or coordination',
                'Physical training or practice'
            ],
            'negative': [
                'Physical disability or limitation',
                'Lack of physical training',
                'Physical fatigue or exhaustion',
                'Physical discomfort when performing'
            ]
        },
        'Capability - Psychological': {
            'positive': [
                'Knowledge of how to perform behavior',
                'Understanding of concepts',
                'Ability to remember or recall information',
                'Mental capacity to engage with the task',
                'Decision-making skills',
                'Interpersonal skills',
                'Behavioral regulation'
            ],
            'negative': [
                'Confusion or misunderstanding',
                'Knowledge gaps',
                'Cognitive overload',
                'Forgetfulness',
                'Mental fatigue'
            ]
        },
        'Opportunity - Physical': {
            'positive': [
                'Available resources',
                'Accessible environment',
                'Available time',
                'Appropriate physical cues',
                'Facilitating environmental factors'
            ],
            'negative': [
                'Lack of resources',
                'Inaccessible environment',
                'Time constraints',
                'Absence of cues',
                'Environmental barriers'
            ]
        },
        'Opportunity - Social': {
            'positive': [
                'Social support',
                'Social norms supporting behavior',
                'Cultural acceptance',
                'Peer encouragement',
                'Role models demonstrating behavior'
            ],
            'negative': [
                'Social disapproval',
                'Cultural barriers',
                'Peer pressure against behavior',
                'Lack of social support',
                'Contradicting social norms'
            ]
        },
        'Motivation - Automatic': {
            'positive': [
                'Positive emotions associated with behavior',
                'Established habits',
                'Desire or craving',
                'Automatic responses',
                'Enjoyment of behavior'
            ],
            'negative': [
                'Fear or anxiety',
                'Competing impulses',
                'Negative emotional associations',
                'Aversion to behavior',
                'Discomfort'
            ]
        },
        'Motivation - Reflective': {
            'positive': [
                'Belief in capability (self-efficacy)',
                'Belief in positive outcomes',
                'Clear intentions',
                'Personal identity aligned with behavior',
                'Goals related to behavior',
                'Optimism about success'
            ],
            'negative': [
                'Low confidence in ability',
                'Pessimism about outcomes',
                'Conflicting goals or intentions',
                'Behavior conflicts with identity',
                'Low priority compared to other goals'
            ]
        }
    }
    
    # Add all indicators to the database
    for category_name, indicator_types in indicators_data.items():
        category = categories[category_name]
        
        for indicator_type, texts in indicator_types.items():
            for text in texts:
                indicator = Indicator(
                    category_id=category.id,
                    text=text,
                    indicator_type=indicator_type
                )
                session.add(indicator)
    
    # Commit the changes
    session.commit()

def populate_coding_examples(session, categories):
    """
    Add example coded text for each category.
    """
    examples_data = {
        'Capability - Physical': [
            {
                'text': 'I find it difficult to take my medication because my arthritis makes it hard to open the pill bottles.',
                'explanation': 'Refers to a physical limitation (arthritis) that impedes the physical ability to perform a task.'
            },
            {
                'text': 'After practicing the injection technique several times with the nurse, I feel confident in my ability to do it correctly.',
                'explanation': 'Indicates physical skill development through practice.'
            }
        ],
        'Capability - Psychological': [
            {
                'text': 'I dont really understand how this medication works or why I need to take it at specific times.',
                'explanation': 'Shows a lack of knowledge or understanding about the treatment.'
            },
            {
                'text': 'I learned the warning signs to watch for and now I know exactly when I need to use my rescue inhaler.',
                'explanation': 'Demonstrates knowledge acquisition and decision-making ability.'
            }
        ],
        'Opportunity - Physical': [
            {
                'text': 'The clinic is an hour drive away and I do not have a car, so I often miss appointments.',
                'explanation': 'Describes a physical environment barrier (distance) and resource limitation (lack of transportation).'
            },
            {
                'text': 'I set an alarm on my phone that reminds me to take my medication every morning.',
                'explanation': 'References an environmental cue (alarm) that facilitates the behavior.'
            }
        ],
        'Opportunity - Social': [
            {
                'text': 'None of my friends exercise regularly, so it is hard to stay motivated when everyone around me is sedentary.',
                'explanation': 'Indicates a lack of social support and negative social norms.'
            },
            {
                'text': 'My support group makes it easier to stick to my diet because we share recipes and encourage each other.',
                'explanation': 'Shows positive social support and community reinforcement.'
            }
        ],
        'Motivation - Automatic': [
            {
                'text': 'I get anxious whenever I think about checking my blood sugar levels because I am afraid of what the reading might show.',
                'explanation': 'Describes negative emotions (anxiety, fear) that automatically inhibit behavior.'
            },
            {
                'text': 'Ive been walking after dinner for so long now that I just do it without thinking - it feels strange if I dont.',
                'explanation': 'Indicates an established habit that motivates behavior automatically.'
            }
        ],
        'Motivation - Reflective': [
            {
                'text': 'I am committed to following my treatment plan because I believe it will help me live longer to see my grandchildren grow up.',
                'explanation': 'Shows conscious intention and belief in positive outcomes aligned with personal goals.'
            },
            {
                'text': 'I do not see myself as the kind of person who needs medication to function properly.',
                'explanation': 'Indicates identity beliefs that conflict with the target behavior.'
            }
        ]
    }
    
    # Add all examples to the database
    for category_name, examples in examples_data.items():
        category = categories[category_name]
        
        for example in examples:
            coding_example = CodingExample(
                category_id=category.id,
                text=example['text'],
                explanation=example['explanation']
            )
            session.add(coding_example)
    
    # Commit the changes
    session.commit()

if __name__ == "__main__":
    # Get a database session
    session = setup_database()
    
    # Populate the database with COM-B data
    categories = populate_comb_categories(session)
    
    # Populate indicators and examples
    populate_indicators(session, categories)
    populate_coding_examples(session, categories)
    
    print("COM-B framework data added to the database successfully!")