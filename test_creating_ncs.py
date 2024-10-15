user_input = """                                                                                                                                    
 Slide 0: Title slide                                                                       
- Title: UAT Reporting for Project NILA Test Cases                                            

 Slide 1: Introduction                                                                       
- Overview of Project NILA                                                                   
- Purpose of UAT User Acceptance Testing                                                     
- Importance of UAT in the project lifecycle                                                 

 Slide 2: UAT Objectives                                                                     
- Validate end-to-end business processes                                                     
- Ensure system meets user requirements                                                      
- Identify and resolve defects before production                                             
- Gain user confidence and acceptance                                                        
                                                                                             
 Slide 3: UAT Scope                                                                          
- Modules and functionalities covered                                                        
- In-scope vs. out-of-scope items                                                            
- Test environments and data                                                                 
                                                                                             
 Slide 4: UAT Test Cases                                                                     
- Total number of test cases                                                                 
- Types of test cases functional, non-functional, regression                                 
- Test case prioritization high, medium, low                                                 
                                                                                             
 Slide 5: UAT Execution Plan                                                                 
- UAT schedule and timeline                                                                  
- Roles and responsibilities                                                                 
- Test execution process                                                                     
- Defect management process                                                                  
                                                                                             
 Slide 6: UAT Results Summary                                                                
- Test case execution status passed, failed, blocked                                         
- Defect summary total defects, severity, status                                             
- Key findings and observations 

Slide 7: Defect Analysis                                                                    
- Defect categorization by module, severity, type                                            
- Root cause analysis                                                                        
- Impact assessment                                                                          
                                                                                             
 Slide 8: User Feedback                                                                      
- Summary of user feedback                                                                   
- User satisfaction ratings                                                                  
- Key concerns and suggestions                                                               
                                                                                             
 Slide 9: Risk and Mitigation                                                                
- Identified risks during UAT                                                                
- Mitigation strategies                                                                      
- Contingency plans                                                                          
                                                                                             
 Slide 10: Recommendations and Next Steps                                                    
- Recommendations for improvement                                                            
- Action items for defect resolution                                                         
- Plan for re-testing and validation                                                         
- GoNo-Go decision criteria                                                                  
                                                                                             
 Slide 11: Conclusion                                                                        
- Recap of UAT objectives and outcomes                                                       
- Importance of UAT in ensuring project success                                              
- Acknowledgments and thanks                                                                 
                                                                                             
 Slide 12: QA                                                                                
- Open floor for questions and answers   
"""


from ncsgpt_potion import ncspotion


design = ncspotion.design(user_input)

print(design)