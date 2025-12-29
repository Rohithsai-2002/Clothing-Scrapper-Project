# PowerShell script to create a Windows Task Scheduler task for the scraper
# Run this as Administrator

$projectPath = "c:\Users\rohit\OneDrive\Documents\Spam_Detection_Project"
$scriptPath = "$projectPath\run_scraper.bat"
$taskName = "ClothingOffersNotifier"
$taskDescription = "Fetch clothing offers and send email alerts"

# Create a trigger for every 1 hour starting now
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

# Create action to run the batch script
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $projectPath

# Create task settings
$settings = New-ScheduledTaskSettingsSet -RunOnlyIfNetworkAvailable -StartWhenAvailable

# Register the task
Register-ScheduledTask -TaskName $taskName `
    -Description $taskDescription `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -RunLevel Highest `
    -Force

Write-Host "Task '$taskName' created successfully!"
Write-Host "The scraper will run every 1 hour."
Write-Host "To modify frequency, open Task Scheduler and edit the trigger."
