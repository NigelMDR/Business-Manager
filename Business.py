class Business:
  def __init__(self, name, income, cost, tax, employee_tax, tot_debt, monthly_debt):
    self.name = name
    self.employee = {}
    self.id = 1
    self.income = income
    self.cost = cost
    self.tax = tax
    self.employee_tax = employee_tax
    self.tot_debt = tot_debt
    self.monthly_debt = monthly_debt
    self.tot_employee_salary = 0
    self.tot_employee_contribution = 0
    
  def add_employee(self, Name:str, Contribution: float):
    salary = round(Contribution*self.employee_tax,2)
    self.employee[Name] = {'Salary': salary, 'Tax': self.employee_tax, 'Contribution': Contribution, 'diff': round(Contribution-salary,2)}
    self.tot_employee_salary += Contribution*self.employee_tax # Employee salary
    self.tot_employee_contribution += Contribution
    self.id += 1
  
  def delete_employee(self, Name):
    del self.employee[Name.lower()]
    
  def get_employees(self):
    return self.employee
    
  def get_stats(self):
    self.stats = {}
    temp = 0
    self.stats['revenue'] = {'#': round(self.income*(1-self.tax),2),
                             '%': -1*self.tax*100}
    # It is typically used to evaluate how efficiently a company is managing labor and supplies in production
    self.stats['gross profit'] = {'#': round(self.stats['revenue']['#'] - self.cost - self.tot_employee_salary,2), 
                                  '%': round((self.stats['revenue']['#'] - self.cost - self.tot_employee_salary)/abs(self.stats['revenue']['#'])*100,2)}
    # % = gross profit_margin above
    # self.stats['gross profit_margin'] = {'%': round(self.stats['gross profit']['#']/self.stats['revenue']['#']*100,2)}
                                        
    # Net Income aka bottom line
    temp = round(self.stats['gross profit']['#'] - self.monthly_debt,2)
    self.stats['net income'] = {'#': temp, 
                                '%': round(temp/abs(self.stats['gross profit']['#'])*100,2)}
  
    # Individual parts: what % of Revenue is spent on each
    temp = round(self.stats['revenue']['#'] - self.cost, 2)
    temp2 = round(self.stats['revenue']['#'],2)
    temp_percent = round((1-temp/temp2)*100,2)
    
    self.stats['Operating Cost'] = {'#': self.cost, 
                                  '%': temp_percent if temp > 0 else -1*temp_percent}
    
    temp = round(temp2 - self.tot_employee_salary, 2)
    temp_percent = round((1-temp/temp2)*100,2)
    self.stats['Employee Cost'] = {'#': self.tot_employee_salary, 
                                  '%': temp_percent if temp > 0 else -1*temp_percent}
    
    temp = round(temp2 - self.monthly_debt,2)
    temp_percent = round((1-temp/temp2)*100,2)
    self.stats['Bank Debt'] = {'#': self.tot_debt - self.monthly_debt, 
                                '%': temp_percent if temp > 0 else -1*temp_percent}
    
    self.stats['Employees Salary'] = self.tot_employee_salary
    return self.stats
  
  def __str__(self):
    self.get_stats()
    return self.name + '/n' + str(self.employee) + str(self.stats)
  