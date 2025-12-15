# Backup and Restore Procedures

## Backup Process

### Full Backup
```bash
# Create backup directory structure
mkdir -p backup/docs/ros2-nervous-system backup/docs/digital-twin backup/docs/ai-robot-brain backup/docs/vla

# Copy all MD and MDX files to backup
cp docs/ros2-nervous-system/*.md* backup/docs/ros2-nervous-system/
cp docs/digital-twin/*.md* backup/docs/digital-twin/
cp docs/ai-robot-brain/*.md* backup/docs/ai-robot-brain/
cp docs/vla/*.md* backup/docs/vla/
```

### Backup Script
A backup script is located at `scripts/backup-content.sh` that can be run with:
```bash
bash scripts/backup-content.sh
```

## Restore Process

### Full Restore
```bash
# Restore all MD and MDX files from backup
cp backup/docs/ros2-nervous-system/*.md* docs/ros2-nervous-system/
cp backup/docs/digital-twin/*.md* docs/digital-twin/
cp backup/docs/ai-robot-brain/*.md* docs/ai-robot-brain/
cp backup/docs/vla/*.md* docs/vla/
```

### Restore Script
A restore script is located at `scripts/restore-content.sh` that can be run with:
```bash
bash scripts/restore-content.sh
```

## Verification
After any restore operation, verify content integrity by:
1. Running `npm run lint-mdx-check` to validate MDX syntax
2. Running `npm run check-links` to validate internal links
3. Checking that the Docusaurus build completes successfully

## Best Practices
- Always create a backup before making significant changes
- Verify backups by ensuring all files are copied correctly
- Test restores on a copy of the repository before using in production
- Document the reason for any backup/restore operation